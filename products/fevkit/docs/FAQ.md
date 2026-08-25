# FAQ

## Does PASS mean the science is correct?

No. PASS means the captured bundle satisfied deterministic audit rules for the selected profile.

## Does V2 mean anyone can reproduce it?

No. V2 means declared files, environment pins, command, and expected artifacts support replay under the captured assumptions.

## Does the browser upload data?

No. The inspector reads the selected JSON in browser memory and has no upload endpoint.

## Is replay safe for untrusted code?

No. It is opt-in and guarded, but not sandboxed.

## Why no trust score?

Because capability, evidence, and validation failures are not interchangeable. A single number would hide the review target.