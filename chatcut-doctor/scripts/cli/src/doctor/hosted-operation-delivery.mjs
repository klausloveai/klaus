import { readFile } from "node:fs/promises";

import { normalizeTarget, sanitize, sha256 } from "./cases.mjs";
import { fragmentEvents } from "./hosted/mcp-doctor.mjs";
import {
  createDoctorFileStorage,
  hostedTelemetryDirectory,
} from "./transport-storage.mjs";

const SMALL_EVENT_BYTES = 24_000;
const MAX_PAYLOAD_BYTES = 128 * 1024;
const DATASET = "chatcut-session";

export async function deliverHostedOperation(info, operation, options = {}) {
  const target = normalizeTarget(info.manifest.target);
  if (target.surface !== "hosted" || !target.endpoint)
    return {
      evidenceGap: "selected_hosted_endpoint_unavailable",
      outcome: "unavailable",
    };
  const env = options.env ?? process.env;
  const state = options.state;
  const currentConnection = state?.observations.findLast(
    (entry) =>
      typeof entry.after?.enabled === "boolean" ||
      typeof entry.lookup?.enabled === "boolean" ||
      entry.outcome === "intentionally_disabled" ||
      entry.report?.integrations?.[target.host]?.status === "opted-out",
  );
  const connectionEnabled =
    currentConnection?.after?.enabled ?? currentConnection?.lookup?.enabled;
  if (
    env.CHATCUT_MCP_TELEMETRY_ENABLED === "0" ||
    env.DISABLE_TELEMETRY === "1" ||
    target.enabled === false ||
    connectionEnabled === false ||
    currentConnection?.outcome === "intentionally_disabled" ||
    currentConnection?.report?.integrations?.[target.host]?.status ===
      "opted-out"
  )
    return { outcome: "disabled", storageVerified: false };
  const relay = new URL("/relay/a", target.endpoint).href;
  const directory = hostedTelemetryDirectory(target.hostHome, relay);
  const storage = createDoctorFileStorage(directory);
  const { createFrontendTransport } =
    await import("./frontend-transport.generated.mjs");
  const manifest = JSON.parse(
    await readFile(
      new URL("./frontend-transport.generated.manifest.json", import.meta.url),
      "utf8",
    ),
  );
  const delivered = new Map();
  const transport = createFrontendTransport(relay, true, {
    fetch: (url, init) =>
      (options.fetch ?? fetch)(url, {
        ...init,
        credentials: "omit",
        keepalive: false,
      }),
    isOnline: options.isOnline ?? (() => true),
    now: options.now,
    onDelivery: (id, outcome, event) => delivered.set(id, { event, outcome }),
    setTimeout(callback, milliseconds) {
      const timer = setTimeout(callback, milliseconds);
      timer.unref();
      return timer;
    },
    storage,
    subscribeOnline: () => undefined,
  });
  let deadline;
  async function drain() {
    deadline ??=
      Date.now() + Math.min(1500, Math.max(0, options.budgetMs ?? 800));
    while (Date.now() < deadline) {
      const before = delivered.size;
      let wait;
      try {
        await Promise.race([
          transport.flush(),
          new Promise((resolve) => {
            wait = setTimeout(resolve, Math.max(0, deadline - Date.now()));
          }),
        ]);
      } finally {
        if (wait) clearTimeout(wait);
      }
      if (!transport.getDeliveryStatus().pending || delivered.size === before)
        break;
    }
  }
  function fits(packets) {
    const budget = transport.getPendingBudget();
    const sizes = packets.map((event) =>
      transport.estimateEvent(DATASET, event, event.eventId),
    );
    return (
      budget.persistent &&
      budget.entries + packets.length <= budget.maxEntries &&
      budget.bytes + sizes.reduce((total, size) => total + size.bytes, 0) <=
        budget.maxBytes &&
      budget.storedBytes +
        sizes.reduce((total, size) => total + size.storedBytes, 0) <=
        budget.maxBytes
    );
  }
  let plan;
  let enqueued = false;
  let resumedExistingPackets = false;
  let admissionGap;
  try {
    if (operation) {
      plan = operationPackets(info, operation, env, manifest);
      resumedExistingPackets = transport
        .getPendingEventIds()
        .some(
          (id) =>
            id === operation.eventId ||
            id === `${operation.eventId}-gap` ||
            id.startsWith(`${operation.eventId}-part-`),
        );
      if (!resumedExistingPackets && !fits(plan.packets)) await drain();
      if (!resumedExistingPackets && !fits(plan.packets) && plan.gap) {
        const emptyBudget = transport.getPendingBudget();
        const sizes = plan.packets.map((event) =>
          transport.estimateEvent(DATASET, event, event.eventId),
        );
        const intrinsic =
          sizes.reduce((total, size) => total + size.storedBytes, 0) >
            emptyBudget.maxBytes ||
          sizes.reduce((total, size) => total + size.bytes, 0) >
            emptyBudget.maxBytes;
        admissionGap = intrinsic
          ? "operation_payload_exceeds_shared_queue_byte_budget"
          : "existing_pending_operations_exhaust_shared_queue_capacity";
        plan = {
          ...plan,
          metadataOnly: true,
          packets: [plan.gap(admissionGap)],
        };
      }
      if (!resumedExistingPackets) {
        if (fits(plan.packets))
          enqueued = plan.packets
            .map((event) => transport.ingest(DATASET, event, event.eventId))
            .every(Boolean);
        else
          admissionGap ??=
            "shared_queue_capacity_or_durable_storage_unavailable; complete_original_and_operation_preserved_locally";
      }
    }
    await drain();
  } finally {
    transport.dispose();
  }
  const settledEvents = settledOperations(delivered);
  const settled = settledEvents.find(
    (entry) => entry.eventId === operation?.eventId,
  );
  return {
    enqueued,
    eventId: operation?.eventId,
    fragmented: plan?.fragmented ?? false,
    metadataOnly: plan?.metadataOnly ?? false,
    outcome: operation
      ? (settled?.outcome ??
        (enqueued || resumedExistingPackets
          ? plan.metadataOnly
            ? "metadata_pending_only"
            : "pending"
          : "not_durably_enqueued"))
      : "resumed_existing_queue",
    payloadBytes: plan?.payloadBytes,
    resumedExistingPackets,
    settledEvents,
    ...(admissionGap ? { evidenceGap: admissionGap } : {}),
    relay,
    status: transport.getDeliveryStatus(),
    storageVerified: false,
    supportBoundary:
      "bounded_shared_transport_batches; pending_recovers_on_later_selected_host_Doctor_calls; fragment_receipts_observed_only_in_this_invocation",
    transportSourceSha256: manifest.sourceSha256,
  };
}

function operationPackets(info, operation, env, manifest) {
  const payload = sanitize({
    ...operation,
    collectedAt: operation.finishedAt,
    diagnosticId: operation.eventId,
    evidenceGaps: [
      ...(operation.evidenceGaps ?? []),
      "hosted_user_identity_unobserved; telemetry_is_not_evidence_access_authorization",
      ...(!env.CHATCUT_MCP_TELEMETRY_STAGE
        ? ["producer_stage_unavailable"]
        : []),
      ...(!env.CHATCUT_MCP_TELEMETRY_COMMIT_SHA
        ? ["producer_commit_unavailable"]
        : []),
    ],
    host: info.manifest.target.host,
    originalFailure: {
      error: info.original.record?.error ?? null,
      failureEventId: info.original.record?.failureEventId,
      occurredAt: info.original.record?.occurredAt,
      operation: info.original.record?.operation,
      source: info.original.record?.source,
      status: info.original.status,
    },
    schemaVersion: 1,
    transportSourceSha256: manifest.sourceSha256,
  });
  const base = {
    _time: operation.finishedAt,
    eventName: "mcp.doctor.operation_result",
    service: "chatcut-cli",
    source: operation.source,
    ...(env.CHATCUT_MCP_TELEMETRY_STAGE
      ? { stage: env.CHATCUT_MCP_TELEMETRY_STAGE }
      : {}),
    ...(env.CHATCUT_MCP_TELEMETRY_COMMIT_SHA
      ? { commitSha: env.CHATCUT_MCP_TELEMETRY_COMMIT_SHA }
      : {}),
    operation: operation.action,
    outcome: operation.outcome,
    requestId: operation.requestId,
  };
  const json = JSON.stringify(payload);
  const payloadBytes = Buffer.byteLength(json);
  const single = { ...base, attributesJson: json, eventId: operation.eventId };
  const gap = (reason) => ({
    ...base,
    attributesJson: JSON.stringify({
      baseEventId: operation.eventId,
      caseId: operation.caseId,
      evidenceGaps: [
        reason,
        "complete_original_and_operation_preserved_locally",
        ...payload.evidenceGaps,
      ],
      localPayloadSha256: sha256(json),
      originalSha256: operation.originalSha256,
      payloadBytes,
      targetFingerprint: operation.targetFingerprint,
      transportSourceSha256: manifest.sourceSha256,
    }),
    eventId: `${operation.eventId}-gap`,
    eventName: "mcp.doctor.operation_result_gap",
  });
  if (payloadBytes > MAX_PAYLOAD_BYTES)
    return {
      metadataOnly: true,
      packets: [
        gap("operation_payload_exceeds_bounded_128KiB_producer_budget"),
      ],
      payloadBytes,
    };
  if (Buffer.byteLength(JSON.stringify(single)) <= SMALL_EVENT_BYTES)
    return { gap, packets: [single], payloadBytes };
  const packets = fragmentEvents(payload).map(({ properties }) => {
    const fragment = properties.attributes.mcpDoctor;
    return {
      ...base,
      attributesJson: JSON.stringify({
        baseEventId: operation.eventId,
        caseId: operation.caseId,
        mcpDoctor: fragment,
        originalSha256: operation.originalSha256,
        targetFingerprint: operation.targetFingerprint,
      }),
      eventId: `${operation.eventId}-part-${fragment.fragmentIndex}`,
      eventName: "mcp.doctor.operation_result_fragment",
    };
  });
  return { fragmented: true, gap, packets, payloadBytes };
}

function settledOperations(delivered) {
  const operations = new Map();
  for (const [id, receipt] of delivered) {
    if (
      ![
        "mcp.doctor.operation_result",
        "mcp.doctor.operation_result_fragment",
        "mcp.doctor.operation_result_gap",
      ].includes(receipt.event.eventName)
    )
      continue;
    const match = /^(doctor-[a-f0-9]{64})(?:-gap|-part-\d+)?$/.exec(id);
    if (!match) continue;
    const eventId = match[1];
    const group = operations.get(eventId) ?? {
      acceptedPartIds: [],
      eventId,
      rejectedPartIds: [],
    };
    let attributes;
    try {
      attributes = JSON.parse(receipt.event.attributesJson);
    } catch {
      continue;
    }
    if (
      receipt.event.eventName === "mcp.doctor.operation_result" &&
      id === eventId
    ) {
      group.outcome =
        receipt.outcome === "accepted"
          ? "accepted_not_storage_verified"
          : "rejected";
    } else if (
      attributes.baseEventId === eventId &&
      receipt.event.eventName === "mcp.doctor.operation_result_gap"
    ) {
      group.outcome =
        receipt.outcome === "accepted"
          ? "metadata_accepted_only"
          : "metadata_rejected";
      group.evidenceGaps = attributes.evidenceGaps;
    } else if (
      attributes.baseEventId === eventId &&
      receipt.event.eventName === "mcp.doctor.operation_result_fragment"
    ) {
      const fragment = attributes.mcpDoctor;
      if (
        id !== `${eventId}-part-${fragment.fragmentIndex}` ||
        !Number.isInteger(fragment.fragmentIndex) ||
        fragment.fragmentIndex < 0 ||
        !Number.isInteger(fragment.fragmentCount) ||
        fragment.fragmentCount < 1 ||
        fragment.fragmentIndex >= fragment.fragmentCount
      )
        continue;
      if (
        group.fragmentCount &&
        (group.fragmentCount !== fragment.fragmentCount ||
          group.payloadSha256 !== fragment.reportSha256)
      )
        continue;
      group.fragmentCount = fragment.fragmentCount;
      group.payloadSha256 = fragment.reportSha256;
      (receipt.outcome === "accepted"
        ? group.acceptedPartIds
        : group.rejectedPartIds
      ).push(id);
    } else continue;
    operations.set(eventId, group);
  }
  return [...operations.values()].map((group) => ({
    ...group,
    outcome:
      group.outcome ??
      (group.acceptedPartIds.length === group.fragmentCount
        ? "accepted_not_storage_verified"
        : group.rejectedPartIds.length
          ? "partly_rejected_or_unknown"
          : "partly_accepted_or_unknown"),
  }));
}
