---
description: Defines the testing requirements to ensure code reliability and maintainability.
---

Use pytest for all tests.

Testing requirements:
- Every public function should have at least one test.
- Test edge cases and failure scenarios.
- Write clear and descriptive test names.

Test naming format:
test_function_scenario

Example:
test_get_prompt_returns_prompt_when_exists

Tests should be placed in the `tests/` directory.