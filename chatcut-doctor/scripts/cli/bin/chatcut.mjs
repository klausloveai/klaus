#!/usr/bin/env node
import { createCliCancellation } from "../src/cli-cancellation.mjs";
import { runCli } from "../src/cli.mjs";

const cancellation = createCliCancellation();
try {
  process.exitCode = cancellation.exitCode(
    await runCli(process.argv.slice(2), {
      get signal() {
        return cancellation.signal;
      },
    }),
  );
} finally {
  cancellation.dispose();
}
