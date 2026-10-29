---
default: major
---

# Use `httpx2` instead of `httpx`

openapi-python-client and the clients it generates now depend on [`httpx2`](https://github.com/pydantic/httpx2),
Pydantic's maintained fork of `httpx` 0.28.1, instead of `httpx`. Generated clients require `httpx2>=2.16.0,<3.0.0`
and import it as `import httpx2 as httpx`, so the generated code and its public API are otherwise unchanged.

`httpx` and `httpx2` objects are distinct classes. If you pass your own client or timeout to a generated client
(`set_httpx_client`, `set_async_httpx_client`, `timeout=`, `with_timeout`) or catch its exceptions (such as
`TimeoutException`), use the `httpx2` versions.

`httpx2` also verifies TLS against the operating system's trust store (via `truststore`) rather than `certifi`,
sends a `python-httpx2/<version>` User-Agent by default, and logs to the `httpx2` / `httpcore2` loggers.
See the [httpx2 migration guide](https://pydantic.dev/docs/httpx2/get-started/migration/) for details.

Docstrings and the generated README now name `httpx2` classes (e.g. `httpx2.TimeoutException`), and the README's
`set_httpx_client` example uses `proxy=` instead of `proxies=`, which no longer exists.
