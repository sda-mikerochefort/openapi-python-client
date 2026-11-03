---
default: patch
---

# Fix duplicate models for unions of inline objects with nested inline objects

A union of inline objects which themselves contained inline objects failed with `Attempted to generate duplicate models`,
and endpoints using the union imported models that were never generated.
