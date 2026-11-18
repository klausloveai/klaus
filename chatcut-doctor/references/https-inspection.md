# HTTPS inspection evidence and recovery

Use this path for an actual native response-body decoding failure or invalid
HTTP framing. Keep the failed service, host/home, scope, account and project.
An installed antivirus product, a certificate issuer, a similar public issue
or an application response log alone cannot establish the responsible component.

## Diagnose the observed boundary

Retain the native error verbatim and its available IDs/times. Later probes are
separate observations, not reconstructed original responses. Invalid chunking
can explain a parser failure when the response claims `Transfer-Encoding:
chunked` but its encoded body starts with unframed JSON. Legal chunked responses
are supported by the tested native Codex client; do not call all chunking broken.

Only the combination of a native failure, independently observed invalid
framing and evidence that an inspection component participates supports the
qualified hypothesis **suspected HTTPS inspection compatibility problem**.
Even that combination does not identify the rewriting hop. A server's
`write/end` observation is before HTTP framing, not Node/ALB egress bytes.
Preserve contradictory or incomplete evidence.

The bundled `scripts/capture-public-framing.cjs` reuses the existing bounded
operation: exactly three anonymous requests, no retry or redirect follow, each
at most 10 seconds/128 KiB, no login, credentials or upload, with TLS verification
retained. It requires existing Node18+ and curl.exe8.4+; it installs neither.
The normal destination is **api.chatcut.io only**. Use it only when that is the
actual failed origin and this later public capture is authorized; do not run it
for a selected beta/dev/other service or silently change targets. `--fixture-origin`
is restricted to owned loopback HTTP tests and does not test real HTTPS scanning.
The [helper provenance](public-framing-provenance.md) pins both script hashes.

```sh
node <this-skill>/scripts/capture-public-framing.cjs --output <new-private-directory>
node <this-skill>/scripts/inspect-capture.mjs <capture-directory>
```

Keep raw bodies, selected framing headers, curl's original stderr, certificates
when actually observed, times and file hashes. Metrics can contain IP addresses;
keep them local until reviewed. The selected-header file is not a complete raw
header capture. The probe's new diagnostic UUID is not the original request ID.
The offline inspector can optionally pair an already-authorized server query;
missing/multiple matches and incomplete captures remain unconfirmed.

## User/IT recovery step

1. Preserve the current failure and before-state. Ask the user/IT to check the
   installed product/version and apply its normal approved updates first. For
   AVG, use the official [update](https://support.avg.com/SupportArticleView?l=en&urlname=update-avg-antivirus)
   and [repair](https://support.avg.com/SupportArticleView?l=en&urlname=repair-avg-antivirus)
   guidance. Repair can reset custom settings, so the operator must retain their
   policy/before-state. Doctor must not run the repair or restart the computer.
2. The vendor's [website-access troubleshooting](https://support.avg.com/SupportArticleView?l=en&urlName=avg-website-access-issues)
   includes temporary comparisons of protection components. The user/IT alone
   decides whether their policy permits such a comparison. Doctor never clicks
   security controls, changes scanning/TLS/proxy/trust settings, installs an
   interceptor, creates broad exceptions or recommends permanent disablement.
   If a temporary comparison is permitted, agree its narrow scope and one-test
   duration, record the exact change, and restore/verify the original protection
   immediately afterward. If it is forbidden, hand the evidence to IT/vendor
   support instead; do not seek a bypass.
3. After the operator reports the actual change and protection state, make a
   fresh safe native read of the same target. Save success **or failure** in this
   case with the actual session boundary. Use `needsUser: true` on an actual
   failed recheck with a concrete `nextAction` when an evidenced human step
   remains. Record the operator's actual change and restored protection state
   in `precedingAction`; in a fixture, name the test controller and fixture-only
   change instead. Only a real native
   success can establish current availability, and it does not by itself locate
   the old rewriting component. Never replay a failed write or generation.

## Evidence and acceptance boundaries

**A — controlled fixture:** malformed wire bytes and a real native/model error
can verify recognition, `needs_user`, an actionable handoff and same-case fresh
reads. A controller changing the fixture to legal framing is a test action,
not Doctor repairing AVG/Avast. Loopback HTTP has no peer TLS certificate; do not
invent one or borrow another machine's issuer to attribute this fixture failure.

**B — affected terminal:** real AVG/Avast recovery needs that terminal's original
failure, bounded before/after observations, exact user/IT operations and restored
protection state, and the original host/target's successful native read. Without
B, mark the antivirus recovery claim unverified. A public [Codex issue](https://github.com/openai/codex/issues/48504)
is a related external report, not a ChatCut customer recovery receipt.

If support needs to locate the rewriting hop, request the selected anonymous
requests' input/output framing from the inspection operator/vendor. Do not
collect unrelated traffic, cookies, private keys or session secrets. This path
does not create production packet capture, a new collector or a new repair rule.
