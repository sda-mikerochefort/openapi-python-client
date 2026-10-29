---
default: patch
---

# Generated clients stay valid with Ruff 0.16 and later

Ruff 0.16 enables many more rules by default and formats Python code blocks in Markdown files. When a client was
generated with `--meta none` into a folder with no Ruff configuration, the default `ruff check . --fix-only` post hook
rewrote `Client.__exit__` / `__aexit__` (rule `PYI036`) in a way that no longer passed `mypy --strict`. These methods
now declare the standard `exc_type`, `exc_value` and `traceback` parameters, so Ruff has nothing to rewrite.

The Python examples in the generated README are now already formatted, so Ruff 0.16+ no longer rewrites them and
generated READMEs are the same regardless of which Ruff version is installed.
