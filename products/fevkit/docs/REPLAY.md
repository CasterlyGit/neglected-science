# Replay contract

Replay is preflight-only by default. Execution requires `--execute`.

The command must be an argument array. The runner copies the bundle to a temporary directory, uses `shell=False`, restricts executables by name, reduces inherited environment variables, enforces a timeout, and compares declared expected artifacts by SHA-256.

These controls are not a sandbox. Network, kernel, process, and hardware isolation require an external execution environment.