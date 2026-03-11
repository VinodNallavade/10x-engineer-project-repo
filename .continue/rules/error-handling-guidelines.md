---
description: Defines how exceptions and errors should be handled to improve debugging and reliability.
---

Handle errors explicitly and avoid silent failures.

Guidelines:
- Validate inputs early.
- Raise meaningful exceptions with clear error messages.
- Never silently ignore exceptions.

Examples:
- Use ValueError for invalid input.
- Use RuntimeError for unexpected failures.

Example:
if not prompt_id:
    raise ValueError("prompt_id cannot be empty")