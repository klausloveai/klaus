---
name: chatcut-web-browser
description: |
  Collect product details, brand assets, page screenshots or video links from a URL (网页素材/品牌资料/网页截图) for a ChatCut project using Firecrawl. Only within a ChatCut media task; general browsing, research and screenshots use the host's web tools.
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


# Web Browser

Web content extraction powered by Firecrawl. Routed through ChatCut's backend proxy, with no provider key stored in Desktop.

Call the MCP tool directly:

```ts
web_browser({ url: "<url>", formats: [...], ...options })
```

For screenshots, the tool returns `data.screenshot` as a remote URL. Download it to a readable local path, then register it with Desktop `push_asset` if the user needs it in the project.

## Formats

Pass any combination of these in the `formats` array. Each appears as a field in `data` on the response:

| Format       | Field             | Returns                                                                                                                    |
| ------------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `markdown`   | `data.markdown`   | Clean LLM-ready text (default if `formats` omitted)                                                                        |
| `html`       | `data.html`       | Cleaned HTML (scripts/styles removed, relative URLs resolved)                                                              |
| `rawHtml`    | `data.rawHtml`    | Unmodified original HTML                                                                                                   |
| `images`     | `data.images`     | Array of image URL strings (use this instead of manually parsing HTML)                                                     |
| `links`      | `data.links`      | Array of hyperlink URL strings found on the page                                                                           |
| `branding`   | `data.branding`   | Structured brand data: `logo`, `colors` (primary/secondary/accent/background/text), `typography`, `spacing`                |
| `summary`    | `data.summary`    | AI-generated page summary                                                                                                  |
| `screenshot` | `data.screenshot` | Remote page screenshot URL. Combined with `fullPage: true` for the entire scrollable page; download locally before import. |
| `videos`     | via `execJs`      | Convenience: injects a video-URL extraction script. Result lands under `data.actions.javascriptReturns[0].value`.          |

## Options

| Option            | Type     | Purpose                                                             |
| ----------------- | -------- | ------------------------------------------------------------------- |
| `waitFor`         | number   | ms to wait for page load before extraction                          |
| `timeout`         | number   | Request timeout (ms)                                                |
| `country`         | string   | Geo-location proxy code, e.g. `US`                                  |
| `onlyMainContent` | boolean  | Strip nav, footers, ads                                             |
| `execJs`          | string   | Run JS in browser before extraction                                 |
| `fullPage`        | boolean  | Capture entire scrollable page (use with `formats: ["screenshot"]`) |
| `actions`         | object[] | Firecrawl actions array (scroll, click, wait, screenshot)           |
| `query`           | string   | Natural-language structured-extraction prompt                       |
| `schema`          | object   | JSON schema for structured extraction                               |

## Key Examples

```ts
// Full-page screenshot URL; download it locally before asset import
web_browser({
  url: "https://example.com",
  formats: ["screenshot"],
  fullPage: true,
  waitFor: 3000,
});
// → { data: { screenshot: "<url>" } }

// Brand assets + images + content (single call)
web_browser({
  url: "https://example.com",
  formats: ["branding", "images", "markdown"],
});

// Structured extraction by prompt
web_browser({
  url: "https://example.com/product",
  query: "Extract: product name, price, rating",
});

// Structured extraction by schema
web_browser({
  url: "https://example.com/product",
  schema: {
    type: "object",
    properties: {
      name: { type: "string" },
      price: { type: "string" },
      features: { type: "array", items: { type: "string" } },
    },
  },
});

// Extract video URLs from a page with dynamic content
web_browser({
  url: "https://example.com",
  formats: ["videos"],
  waitFor: 3000,
});

// Scroll + screenshot via actions
web_browser({
  url: "https://example.com",
  formats: ["screenshot"],
  actions: [
    { type: "wait", milliseconds: 2000 },
    { type: "scroll", direction: "down", amount: 3 },
    { type: "screenshot", fullPage: true },
  ],
});
```

## Error Handling

| Scenario      | Action                                                  |
| ------------- | ------------------------------------------------------- |
| Timeout / 5xx | Retry with `waitFor: 5000, timeout: 60000`              |
| Empty result  | Retry with `country: "US"`                              |
| 403 / blocked | Try `actions` with wait + scroll, or `execJs`           |
| SPA lazy-load | Use `waitFor: 3000` or `actions` with scroll to trigger |
| No video URLs | Pass `formats: ["videos"]` + `waitFor: 5000`            |

## Notes

- No setup: Firecrawl key lives in the backend proxy, not in the agent.
- `country` is auto-applied for known geo-blocked sites (Amazon, Walmart, eBay, etc.). Pass `country` explicitly to override.
- `execJs` runs JavaScript BEFORE content extraction. Return value at `data.actions.javascriptReturns`.
- `actions` takes raw Firecrawl actions JSON. See [Firecrawl docs](https://docs.firecrawl.dev/features/scrape#actions) for all action types.
- Use `formats: ["images"]` to get image URLs directly. Do NOT parse HTML manually.
- When `actions` is provided, `execJs` and the `videos` convenience are ignored (actions takes full control).
- Image URLs returned in `data.images` are remote. Download a selected image to a readable local path, then call Desktop `push_asset` with the local file path.
