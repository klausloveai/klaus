export const CLIENT_FAMILIES = {
  "claude-code": "claudeCode",
  codex: "chatGpt",
  "deepseek-harness": "deepseekHarness",
  "doubao-work": "doubaoWork",
  hermes: "hermes",
  "qwen-work": "qwenWork",
  workbuddy: "workBuddy",
};
export const CLIENTS = Object.keys(CLIENT_FAMILIES);

export const CLIENT_RELOAD_GUIDANCE = {
  "claude-code": {
    action: "restart-agent-session",
    displayName: "Claude Code",
    evidence: "adapter-reported; native acceptance pending",
    instruction:
      "Ask the user to exit and reopen the Claude Code agent session after connection changes. Do not substitute clearing the conversation for restarting the session.",
  },
  codex: {
    action: "restart-agent-session",
    displayName: "Codex",
    evidence:
      "native Codex CLI 0.160.1 fresh-session skill/tool call verified; desktop app reload acceptance pending",
    instruction:
      "For Codex CLI, ask the user to exit and reopen the agent session after connection changes; merely clearing the conversation is not a verified MCP reload. In the Codex desktop app, first prepare a new conversation and verify its tools; if they are still absent, ask the user to restart Codex. Desktop app reload acceptance is still pending, so do not promise that a new chat alone is sufficient.",
  },
  "deepseek-harness": {
    action: "native-setup-required",
    displayName: "DeepSeek Harness",
    evidence:
      "real Desktop Agent completed CLI connect and bundled skill read; native macOS 0.2.1-rc.3 tool-table registration remains unresolved",
    instruction:
      "Continue through the ChatCut CLI from the local shell. The current Desktop-profile adapter has not established native tool-table access, so do not promise that restarting fixes it or ask for repeated restarts.",
  },
  "doubao-work": {
    action: "new-conversation",
    displayName: "Doubao Work",
    evidence: "native-verified on macOS 2.34.9",
    instruction:
      "Continue in a new Doubao Work task after connector installation; an already-running task retains its old tool table. Prepare the new task automatically when possible, otherwise ask the user only to click the prepared continuation link and Send. Restart Doubao only if its system permission screen explicitly requires it.",
  },
  hermes: {
    action: "restart-agent-session",
    displayName: "Hermes",
    evidence:
      "native Hermes 0.22.5 fresh CLI session loaded doctor with skill_view and successfully called the Desktop MCP tool",
    instruction:
      "Ask the user to exit and reopen the Hermes agent session after connection changes so it reloads the MCP configuration and skills.",
  },
  "qwen-work": {
    action: "native-setup-required",
    displayName: "Qwen Work",
    evidence:
      "real macOS 1.4.0 Agent read a bundled skill and called Desktop through CLI; native account-scoped tool-table registration remains unresolved",
    instruction:
      "Continue through the ChatCut CLI from the local shell. New conversations did not load tools from the legacy registration in Qwen Work 1.4.0. Native account-scoped registration needs separate acceptance; do not ask for repeated new conversations as a repair.",
  },
  workbuddy: {
    action: "native-setup-required",
    displayName: "WorkBuddy",
    evidence:
      "native macOS 5.9.3 loaded the skill but lacked ChatCut tools even after app restart and a new task; CLI route is available",
    instruction:
      "Continue through the ChatCut CLI from the local shell. Native registration remains unresolved in WorkBuddy 5.9.3; restarting and opening a new task did not suffice. Do not ask the user for repeated restarts. Approve ChatCut trust only if the host actually requests it.",
  },
};

export function hostHandoff(client, integration) {
  const policy = CLIENT_RELOAD_GUIDANCE[client];
  if (!policy) return undefined;
  return {
    client,
    ...policy,
    agentInstruction:
      "Check your own loaded ChatCut tools and skills first. If both are already usable, do not ask for another restart. When you have a shell on the user's computer, continue immediately with chatcut skills list/read and chatcut tools list/describe/call instead; this CLI route requires no host reload. The host action below is only for loading tools into the native host tool table. If choosing that route, explain its exact action and ask the user to help; do not silently terminate the current host. Preserve the current request in a continuation before that handoff. The user must not copy commands, edit configuration, or re-enter the task.",
    configurationReloadReported: integration.restartRequired === true,
    trustPending: integration.trustPending === true,
    verification:
      "In the resumed host conversation, load a managed ChatCut skill and call get_active_project through the host's actual ChatCut Desktop connector. surface must be desktop; projectId may be null. CLI configuration checks, copied skill files and a standalone MCP probe do not establish host acceptance.",
  };
}
