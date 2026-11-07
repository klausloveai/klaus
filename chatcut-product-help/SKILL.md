---
name: chatcut-product-help
description: |
  Answer questions about ChatCut features, versions, troubleshooting, credits, plans, pricing, billing and setup (使用帮助/版本/积分/订阅/安装) from official docs. Not for live project, asset or timeline state; use the matching read tool.
user-invocable: false
---

## Desktop connection in an external host

Use this procedure only for a ChatCut route compatible with the user's goal.
With working Desktop tools, continue. If tools are missing/disconnected, first
reconnect without installing Desktop:

`npx --yes --prefer-online @chatcut/cli@latest connect --no-install --json`

Use existing authorization for connection and ordinary recovery. Honor actual
host permission requirements without adding a repeated installation approval.
Never remove --no-install to accommodate an older CLI: unguarded connect may
install Desktop. An unsupported flag does not establish that Desktop is absent.
Read-only doctor, an installed trusted launcher and supported host connection
mechanisms can establish availability while the published CLI lacks the guard.

Only an actual Desktop installation requires a host permission click for:

`npx --yes --prefer-online @chatcut/cli@latest connect --allow-install --json`

Explain that this may download/install the signed production Desktop, open it
and connect CLI access. Submit the exact command through the host's supported
permission prompt so the user clicks approval. Auto-allow, standing grants,
bypass mode and a never-approve host cannot supply this installation click.
Do not add permission rules or skill tool pre-approvals. Without a supported
prompt, show the manual command without running it. If installation approval is denied,
respect it; do not retry installation through another tool, installer or flags.
The flag records approval already obtained; it cannot itself prove permission.
Never remove --allow-install or bypass publisher validation to work around a
CLI rejection. Preserve credentials, native-host opt-outs and ownership/path
boundaries during targeted configuration repair.

Check exit code, ok and the original result. Preserve the original error,
diagnose recoverable package, transport or inspection failures within existing
authorization, and inspect current state before retrying an uncertain mutation.
Resume the original task after recovery; continue independent authorized work
when a step remains blocked, honoring any refusal and upload restrictions.
A successful connection proves CLI access separately from native host loading.
Use skills read <name>, tools describe <name> --json and tools call as needed;
preserve projectId and follow actual sign-in/service permission results.
Before any paid generation, obtain a current supported quote for the exact
parameters and explicit approval covering that price and scope. Reuse an
existing approval that still covers the operation; do not invent pricing or
resubmit an uncertain paid job without inspecting its task and billing state.


# ChatCut Product Help

Use current official documentation for product behavior and ChatCut read tools
for live app, project, account or task state. A question only about live state needs
no Docs lookup. For a mixed question, use tools for live state and Docs for its
meaning. The Skill routes to evidence; it does not own prices, UI or versions.

## Read the relevant source

Open a known official page directly. Otherwise use native search and page-reading
capabilities, a connected docs search tool, or the official discovery endpoints:

- `https://chatcut.io/docs/search?q=TOPIC&locale=LOCALE` (URL-encode the topic).
- `https://chatcut.io/docs/llms.txt` (documentation index).

If a discovery endpoint is unavailable, use native search or the HTML Docs index.
Use the search endpoint locale codes `en`, `zh`, `es`, `ja` or `zh-hant`.
Choose the requested language when available; use English for missing translations
and as the authority when translations disagree, explaining the difference.
Prefer a returned or advertised Markdown URL, or try the known page's `.md`
alternate. Read the canonical HTML page if Markdown is missing or unusable.
Use indexes to choose specific pages; avoid `llms-full.txt` for ordinary help questions.
Search snippets and unopened results are discovery, not evidence. Read only the
sources that establish the answer; stop when evidence is sufficient or unavailable.
Cite the canonical human-readable URL supporting consequential claims. If sources
cannot establish the answer, say what is unverified and give the closest official
page or Feedback path. Do not assume an optional MCP server is connected.

For version or rollout questions, read the owning feature guide plus the relevant
entry in `https://chatcut.io/docs/changelog`; `https://chatcut.io/docs/releases`
shows Current versions. Feature Docs own present behavior; the individual change
owns its minimum version. A current release header does not set every feature's
minimum version. State any unresolved disagreement between sources.

## Use the correct surface

Prefer the explicit runtime profile or `[chatcut-runtime]` envelope:
`chatcut-web-editor` means Web; `chatcut-desktop` means Desktop;
`chatcut-workbench-client` and `chatcut-chat-connector` mean Agent Plugin.
Answer for the user's target surface when it differs from the host. Ask which
surface/version they use only when it changes the answer and context is absent.

Web changes arrive server-side. Treat a capability available on Web as available
through Agent Plugin unless official sources say otherwise; service and tool
changes do not require a Plugin update. A standalone Plugin needs an update only
when the individual change names a Plugin minimum because its bundled Skill changed.
Agent Plugin hosted by ChatCut Desktop uses Desktop's bundled Skills: a Desktop
update updates both; never ask the user to update the Plugin separately there.
Compare Desktop/standalone Plugin versions with the documented minimum, and link
the official update steps when needed. A Desktop-only feature requires Desktop;
a release listing a Desktop version does not by itself make it Desktop-only.

## Desktop setup and paid-feature requests

Use `https://chatcut.io/desktop` for installation and connection steps. npm is
optional: if it is unavailable or fails, use the official native installer and
Desktop's **Agents on this computer** controls. Preserve existing projects,
settings, agent configuration and Skills. Install and open Desktop before using
the browser sign-in handoff; verify sign-in inside Desktop before continuing.

When the user's request needs a paid feature, check access after sign-in with
Desktop's `read_billing` and, for a planned generation, `estimate_generation` when
available. Unknown account state or a failed read does not mean Free. Do not ask
for an upgrade for a task the account can already perform.

For a signed-in non-member whose requested feature needs membership, open
`chatcut://billing` through the local computer's URL-opening capability to show
Desktop's billing popup. Prefer a more specific Desktop billing link returned
by a tool. If the link cannot open, use **profile/account row at the bottom-left
of the sidebar → Upgrade**. If app control is unavailable, give those exact
clicks. Desktop's **Credits** menu item opens **Settings → Plan & credits**;
the web editor's top-right avatar instructions describe a different interface.
See `https://chatcut.io/docs/desktop-app#sign-in-and-use-a-paid-feature` and the
current billing docs for details.

Explain the access requirement and let the user choose a plan and complete
checkout. Opening billing does not authorize a purchase. Recheck access after
payment and resume the original request with its existing media and context.
For an existing member who only lacks credits, use the available credit-purchase
options rather than asking them to subscribe again. Quote and obtain approval
before submitting paid generation; never submit just to discover its price.

## Export location, progress, and stuck exports

Use `/docs/exporting` for the panel, `/docs/export-history` for Export queue,
progress, download and retry behavior, and `/docs/web-export-limits` for rendering
location and surface limits; `/docs/desktop-local-export` covers local-file delivery.
These facts stay in Docs rather than this Skill.

Inspect a live export with the loaded status tool: `track_export` on Web or
`track_progress` with `target="export"` and the returned task identifier on Desktop.
Follow the tool's actual schema and coverage. If it cannot see another tab/window,
explain that limit and use the current queue guide. Use returned `outputPath` or
other delivery information; do not invent a path or infer a cause from icon visibility.

## Help the user act

Desktop's `read_project` also discovers editable app preferences and shared local
resources, with their locations and editing contracts.

Complete requested actions through available interfaces. Give manual UI
steps when the user wants guidance or the action cannot be completed directly.
Use current localized UI labels, supported surfaces and verified limits. Live
balances, charges, quotas, subscriptions and installation state require live
evidence. Keep internal implementation and unpublished preview content out of
product answers.
