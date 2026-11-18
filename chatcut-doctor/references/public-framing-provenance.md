# Public framing helper provenance

The two scripts reuse ChatCut's existing 2026-10-28 three-request support
operation. They are byte-identical snapshots, not a new collector, and need no
developer checkout at runtime.

| File                                 | SHA-256                                                            |
| ------------------------------------ | ------------------------------------------------------------------ |
| `scripts/capture-public-framing.cjs` | `1240a7fe95e47277b7efc55157d4e322e56961b0b40012fcc0ed69b9f9439424` |
| `scripts/inspect-capture.mjs`        | `02bf30e0a580751660eca740889d8eaf05dec3e40952da3eacb493a8558398d9` |

The support operation's earlier Windows fixture receipt verified three
anonymous requests, raw malformed/valid chunk captures and omission of injected
credential headers. That receipt is supporting implementation evidence, not
proof of recovery on an affected terminal. This Doctor candidate adds its own
controlled native-model acceptance separately.

The snapshots are excluded from formatting to preserve those bytes. The
capture's default production origin must match the actual failed target and
be authorized before execution. The owned-loopback override is a controlled
test, not HTTPS or antivirus recovery. See [the evidence contract](https-inspection.md)
for limits, privacy, user/IT actions and same-case native verification.
