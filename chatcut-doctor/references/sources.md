# Doctor workflow research

Inspected 2026-10-25. These sources informed the workflow; no upstream code or
substantial text was copied. Repository popularity describes the collection,
not evidence that one skill works. The implementation is original ChatCut code.

- [OMX doctor skill](https://github.com/Yeachan-Heo/oh-my-codex/blob/6b1c110ec06b45a5644ceb6ee60788f7ccae6c46/skills/doctor/SKILL.md)
  and [CLI implementation](https://github.com/Yeachan-Heo/oh-my-codex/blob/6b1c110ec06b45a5644ceb6ee60788f7ccae6c46/src/cli/doctor.ts)
  (MIT; repository observed at 33,631 stars): adapted explicit checks, installed
  version evidence, selected config-home semantics, preserved original failures,
  and before/after repair verification. Rejected broad deletion of user skill
  roots/caches and replacing global instruction files: they exceed ChatCut's
  ownership and do not establish connection recovery.
- [OMC doctor skill](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/5632614b75cc7833f74604be65d26a62a5b773de/skills/omc-doctor/SKILL.md)
  (MIT; repository observed at 40,246 stars): adapted respect for active config
  roots and standing opt-outs, exact ownership evidence before cleanup, and
  preserving ambiguous custom behavior. Omitted its hook migration and global
  instruction management; ChatCut's existing Desktop integration owner remains
  responsible for its own settings.
- [skill-doctor skill](https://github.com/evilstar2016/skill-doctor/blob/dd7e86b5721aa8f4bf7a7b5542b2a5cb5c03373c/skills/skill-doctor/SKILL.md)
  (MIT; repository observed at 13 stars): adapted structured diagnostics,
  path-specific findings, separation of diagnosis from mutation, and the
  distinction between similarity and interchangeability. Rejected installing
  its scanner, model providers or a second central skills library: ChatCut
  already owns its bundled workflows and ownership manifest.
- [OpenClaw doctor](https://docs.openclaw.ai/gateway/doctor) and
  [npm doctor](https://docs.npmjs.com/cli/v11/commands/npm-doctor/): primary
  references for actionable checks and explicit recovery operations. ChatCut
  keeps app update separate from diagnosis, uses bounded local checks and
  preserves the user's existing application state.
- [MCP lifecycle implemented by Desktop](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/lifecycle.mdx):
  the probe negotiates the handshake protocol supported by ChatCut's current
  SDK, lists tools and executes a read. This is protocol-specific evidence,
  not proof of discovery inside another already-running agent conversation.

ChatCut's existing `connect-chatcut-desktop` and hosted MCP doctor materials were
also inspected. Their official artifact selection, truthful handoff and
separation of independent probes from original host failures remain useful.
The new CLI does not reuse the hosted collector, OAuth probes or log-upload
pipeline for local Desktop repair.

Original integration: authenticated operations on Desktop's existing local IPC
reuse its connection and skill owners; the npm CLI only bootstraps the signed
app and verifies observable results. Old ownership hashes are checked against
current bytes before any update/removal. Intentional per-host variants stay
independent. Cross-platform fixture tests do not establish native Windows
installation success; that remains a release acceptance requirement.
