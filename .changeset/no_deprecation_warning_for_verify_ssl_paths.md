---
default: patch
---

# No deprecation warning when `verify_ssl` is a path

httpx2 deprecates passing a CA bundle path as `verify=`. When a generated client's `verify_ssl` is a path to a CA
bundle file or directory, the client now builds the equivalent `ssl.SSLContext` itself, exactly as httpx2 would.
This also allows combining a `verify_ssl` path with `cert=` in `httpx_args`, which httpx2 rejects for `verify=<path>`
(httpx2 still warns that `cert=` itself is deprecated).
