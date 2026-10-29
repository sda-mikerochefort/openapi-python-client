---
default: patch
---

# No deprecation warning for cookie parameters

Generated endpoints with cookie parameters passed `cookies=` to `httpx2.Client.request()`, which httpx2 deprecates.
They now call `build_request()` and `send()`, which `request()` is documented to be equivalent to, so the cookies
are sent exactly as before without a `DeprecationWarning`.

If you mock `get_httpx_client().request` (or the async equivalent) in tests of these endpoints, mock `send` instead.
