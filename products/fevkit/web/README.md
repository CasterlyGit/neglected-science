# Browser inspector

The production browser inspector is deployed at `https://fevkit.vercel.app`.

`index.html` is a no-build artifact. It evaluates user-selected `run.json` files entirely in the browser. Browser inspection is intentionally capped at V1 because it cannot verify adjacent files or execute replay; the Python CLI is canonical for V2 and above.

The production deployment contains no analytics, account system, or upload endpoint. Local files remain in the browser.
