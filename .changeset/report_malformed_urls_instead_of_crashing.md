---
default: patch
---

# Report malformed `--url` values instead of crashing

Some malformed URLs (such as `http://[::1/openapi.json` or `http://example..com/openapi.json`) raised an uncaught
exception with a traceback. They now produce the usual "Could not get OpenAPI document from provided URL" error.
