const SIGNAL_EXIT_CODES = { SIGINT: 130, SIGTERM: 143 };

export function createCliCancellation({
  cleanupTimeoutMs = 10_000,
  process: cliProcess = process,
} = {}) {
  const controller = new AbortController();
  let listening = false;
  let disposed = false;
  let requestedExitCode;
  let deadline;
  const listeners = new Map();
  const cancel = (name) => {
    const code = SIGNAL_EXIT_CODES[name];
    if (controller.signal.aborted) {
      cliProcess.exit(code);
      return;
    }
    requestedExitCode = code;
    deadline = setTimeout(() => cliProcess.exit(code), cleanupTimeoutMs);
    deadline.unref();
    controller.abort(
      new DOMException(`ChatCut Doctor cancelled by ${name}.`, "AbortError"),
    );
  };
  return {
    dispose() {
      disposed = true;
      clearTimeout(deadline);
      for (const [name, listener] of listeners)
        cliProcess.removeListener(name, listener);
      listeners.clear();
    },
    exitCode(code) {
      return requestedExitCode ?? code;
    },
    get signal() {
      // Other CLI commands retain Node's default signal handling.
      if (!listening && !disposed) {
        for (const name of Object.keys(SIGNAL_EXIT_CODES)) {
          const listener = () => cancel(name);
          listeners.set(name, listener);
          cliProcess.on(name, listener);
        }
        listening = true;
      }
      return controller.signal;
    },
  };
}
