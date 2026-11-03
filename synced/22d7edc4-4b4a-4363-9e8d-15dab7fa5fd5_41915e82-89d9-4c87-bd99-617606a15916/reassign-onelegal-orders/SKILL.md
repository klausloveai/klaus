---
name: reassign-onelegal-orders
description: "Reassign One Legal orders from one matter/billing code to another. Use when a case's matter code needs to be corrected or standardized (e.g. 'Dog Bite-Lina Lu-070926' → 'DB-Lina Lu-070926') — navigates to each order and edits the matter number via the browser."
---

# Reassign One Legal Orders to a New Matter/Billing Code

This skill moves One Legal orders from a source matter to a target matter by editing each order's matter number.

## What you need before starting

- **Source matter** — the current (wrong/old) billing code, e.g. `Dog Bite-Lina Lu-070926`
- **Target matter** — the correct billing code to reassign to, e.g. `DB-Lina Lu-070926`
- Already logged in to [platform.onelegal.com](https://platform.onelegal.com) in Chrome (or be prepared to log in)

## Steps

### 1. Load Chrome tools

Load the browser tools before anything else:

```
ToolSearch: select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__find,mcp__claude-in-chrome__javascript_tool
```

### 2. Navigate to the source matter's billing tab

1. Go to `https://platform.onelegal.com/app/Matters`
2. Search for the source matter by name or billing code if it's not immediately visible
3. Click into the source matter
4. Click the **Billing** tab
5. Read the page to get all order numbers listed

### 3. For each order, reassign the matter number

For every order row in the billing table:

1. Click the order number link to open the order detail page
2. On the order detail page, find the **Matter / Billing Code** field on the right sidebar
3. Click the **Edit** link next to it
4. In the dialog, clear the current text and type the first few letters of the **target** billing code
5. Wait for the autocomplete dropdown to appear and select the correct target matter
6. Click **Save**
7. Wait for the "Updating matter number..." toast notification to appear (confirms the save)
8. Click **Back** to return to the source matter's billing tab
9. Repeat for the next order

### 4. Verify

After all orders are reassigned:

1. Confirm the source matter's billing tab now shows 0 orders (or only orders that should remain)
2. Navigate to the target matter and open its **Billing** tab
3. Confirm all reassigned orders now appear there with the correct billing code

## Notes

- One Legal's autocomplete on the Edit matter dialog is triggered by typing — type at least 3–4 characters of the target billing code and wait ~1s for results
- If an order was filed before the target matter existed, the target matter may not appear in autocomplete — you may need to create it first under Matters
- The "Updating matter number" update is async; wait for it before navigating away
- Orders on page 2+ of billing: if the source matter has more than 10 orders, page through all pages before closing out
- This skill covers reassigning from the **order detail page** only — there is no bulk-reassign option in One Legal's UI