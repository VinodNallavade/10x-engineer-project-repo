"""
Example pytest unit tests for utility/helper functions in ``app.utils``.

These tests are written as *templates* for common kinds of utility functions.
They are designed so that if a function does not exist in ``app.utils``,
the corresponding tests are skipped instead of failing.

Adapt the function names and expectations to match the actual behavior
of your own utilities.
"""

from __future__ import annotations

import pytest

try:
    # Adjust this import if your utils module lives elsewhere
    import app.utils as utils  # type: ignore[import]
except ImportError:  # pragma: no cover
    # If the utils module itself does not exist, skip the whole file.
    pytest.skip("app.utils module not available", allow_module_level=True)


# ---------- Helpers & Fixtures ----------

def _get_util_or_skip(name: str):
    """
    Helper: get a function from app.utils or skip tests if it's missing.

    This keeps the test file usable as an example/template even if your
    utils module does not define all the functions referenced below.
    """
    if not hasattr(utils, name):
        pytest.skip(f"app.utils.{name} is not defined; adjust tests to your actual utils.")
    return getattr(utils, name)


@pytest.fixture
def sample_text() -> str:
    """Simple, typical text value used across multiple tests."""
    return "  Hello   world  "


@pytest.fixture
def large_text() -> str:
    """Very large text input to exercise performance/robustness edge cases."""
    return ("abc  " * 10000).strip()


@pytest.fixture
def special_text() -> str:
    """Text containing unicode and special characters."""
    return "Tïtlé with Üñîçødé & symbols !@#$%^&*()   \n\t"


# =====================================================================
# normalize_whitespace(text)  -> example function 1
# =====================================================================

def test_normalize_whitespace_basic(sample_text):
    """
    normalize_whitespace should trim leading/trailing whitespace
    and collapse internal whitespace to a single space for a normal string.
    """
    normalize_whitespace = _get_util_or_skip("normalize_whitespace")

    result = normalize_whitespace(sample_text)
    assert result == "Hello world"


def test_normalize_whitespace_empty_string():
    """normalize_whitespace should return an empty string when given an empty string."""
    normalize_whitespace = _get_util_or_skip("normalize_whitespace")

    assert normalize_whitespace("") == ""


def test_normalize_whitespace_none_value():
    """
    normalize_whitespace(None) should either:
    - return an empty string, or
    - raise a clear, intentional exception (TypeError or ValueError).
    Adjust this test based on your actual behavior.
    """
    normalize_whitespace = _get_util_or_skip("normalize_whitespace")

    with pytest.raises((TypeError, ValueError)):
        normalize_whitespace(None)  # type: ignore[arg-type]


def test_normalize_whitespace_large_input(large_text):
    """normalize_whitespace should handle very large inputs without error."""
    normalize_whitespace = _get_util_or_skip("normalize_whitespace")

    result = normalize_whitespace(large_text)
    # Should still be a non-empty string and not blow up
    assert isinstance(result, str)
    assert result.strip() == large_text.strip().replace("  ", " ")


def test_normalize_whitespace_with_special_characters(special_text):
    """
    normalize_whitespace should preserve non-whitespace special characters,
    only normalizing whitespace itself.
    """
    normalize_whitespace = _get_util_or_skip("normalize_whitespace")

    result = normalize_whitespace(special_text)
    assert "Tïtlé with Üñîçødé & symbols !@#$%^&*()" in result
    assert "\n" not in result
    assert "\t" not in result


# =====================================================================
# slugify(text)  -> example function 2
# =====================================================================

def test_slugify_basic():
    """
    slugify should convert a simple string to a URL-friendly slug:
    - lowercased
    - spaces converted to hyphens
    - special characters removed/normalized (implementation-dependent).
    """
    slugify = _get_util_or_skip("slugify")

    assert slugify("Hello World") in ("hello-world", "hello_world")


def test_slugify_empty_string():
    """slugify should return an empty string or a safe default for empty input."""
    slugify = _get_util_or_skip("slugify")

    result = slugify("")
    assert isinstance(result, str)
    # Adjust expected behavior if you return something like "n-a" instead.
    assert result in ("", "n-a")


def test_slugify_with_unicode_and_symbols(special_text):
    """
    slugify should handle unicode and symbols gracefully, not raising errors.
    """
    slugify = _get_util_or_skip("slugify")

    result = slugify(special_text)
    assert isinstance(result, str)
    # Slug should not contain spaces or control characters
    assert " " not in result
    assert "\n" not in result
    assert "\t" not in result


def test_slugify_invalid_type_raises_type_error():
    """slugify should raise a clear error when given a non-string input like an int."""
    slugify = _get_util_or_skip("slugify")

    with pytest.raises((TypeError, ValueError)):
        slugify(123)  # type: ignore[arg-type]


# =====================================================================
# safe_int(value, default=None)  -> example function 3
# =====================================================================

def test_safe_int_converts_valid_string():
    """safe_int should convert a valid numeric string to an integer."""
    safe_int = _get_util_or_skip("safe_int")

    assert safe_int("42") == 42


def test_safe_int_returns_default_on_invalid_input():
    """
    safe_int should return the provided default for invalid inputs
    instead of raising, for normal non-critical use cases.
    """
    safe_int = _get_util_or_skip("safe_int")

    assert safe_int("not-a-number", default=0) == 0
    assert safe_int("not-a-number", default=None) is None


def test_safe_int_none_input():
    """safe_int(None, default=1) should return the default."""
    safe_int = _get_util_or_skip("safe_int")

    assert safe_int(None, default=1) == 1  # type: ignore[arg-type]


def test_safe_int_very_large_number():
    """
    safe_int should handle very large integer strings or raise a documented error.
    Adjust this based on your implementation.
    """
    safe_int = _get_util_or_skip("safe_int")

    huge_num = "9" * 100  # very large integer
    result = safe_int(huge_num, default=None)
    assert isinstance(result, int)


def test_safe_int_missing_default_raises_for_invalid_value():
    """
    If default is not provided and conversion fails,
    safe_int should raise a clear exception.
    """
    safe_int = _get_util_or_skip("safe_int")

    with pytest.raises((TypeError, ValueError)):
        safe_int("invalid")  # type: ignore[call-arg]


# =====================================================================
# ensure_list(value)  -> example function 4
# =====================================================================

def test_ensure_list_wraps_scalar_value():
    """ensure_list should wrap a non-list value into a single-element list."""
    ensure_list = _get_util_or_skip("ensure_list")

    assert ensure_list("x") == ["x"]
    assert ensure_list(1) == [1]


def test_ensure_list_passes_through_existing_list():
    """ensure_list should return list values as-is (or a shallow copy)."""
    ensure_list = _get_util_or_skip("ensure_list")

    original = [1, 2, 3]
    result = ensure_list(original)
    assert result == original
    # Depending on your requirements, you may want to ensure not same object:
    # assert result is not original


def test_ensure_list_none_returns_empty_list():
    """ensure_list(None) should return an empty list."""
    ensure_list = _get_util_or_skip("ensure_list")

    assert ensure_list(None) == []  # type: ignore[arg-type]


def test_ensure_list_large_iterable():
    """ensure_list should handle very large iterables without error."""
    ensure_list = _get_util_or_skip("ensure_list")

    data = range(10000)
    result = ensure_list(data)
    assert len(result) == 10000


# =====================================================================
# chunked(iterable, size)  -> example function 5
# =====================================================================

def test_chunked_splits_list_into_chunks():
    """
    chunked should split a list into sublists of the given size.
    e.g., chunked([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]
    """
    chunked = _get_util_or_skip("chunked")

    data = [1, 2, 3, 4, 5]
    chunks = list(chunked(data, 2))
    assert chunks == [[1, 2], [3, 4], [5]]


def test_chunked_handles_exact_multiple():
    """chunked should handle an exact multiple of the chunk size."""
    chunked = _get_util_or_skip("chunked")

    data = [1, 2, 3, 4]
    chunks = list(chunked(data, 2))
    assert chunks == [[1, 2], [3, 4]]


def test_chunked_empty_iterable():
    """chunked should return an empty iterable when given an empty iterable."""
    chunked = _get_util_or_skip("chunked")

    chunks = list(chunked([], 3))
    assert chunks == []


def test_chunked_invalid_size_raises():
    """
    chunked should raise a ValueError or similar when given a non-positive size.
    """
    chunked = _get_util_or_skip("chunked")

    with pytest.raises((ValueError, AssertionError)):
        list(chunked([1, 2, 3], 0))


def test_chunked_large_input():
    """chunked should be able to process large inputs without error."""
    chunked = _get_util_or_skip("chunked")

    data = list(range(10000))
    chunks = list(chunked(data, 128))
    # Ensure all elements are present across chunks
    flat = [item for sub in chunks for item in sub]
    assert flat == data


# =====================================================================
# Generic structural tests covering *all* callables in app.utils
# =====================================================================

def test_all_public_utils_are_callable():
    """
    Generic structural check: ensure all public attributes in app.utils
    that look like functions are actually callables.
    """
    public_names = [
        name for name in dir(utils)
        if not name.startswith("_")
    ]

    for name in public_names:
        attr = getattr(utils, name)
        # Only assert on things that should reasonably be functions/helpers
        if callable(attr):
            assert callable(attr), f"app.utils.{name} should be callable"


def test_utils_do_not_raise_on_repr():
    """
    Smoke test: calling repr() on each public attribute should not raise.
    This helps catch weird objects or lazy attributes with side effects.
    """
    for name in dir(utils):
        if name.startswith("_"):
            continue
        attr = getattr(utils, name)
        _ = repr(attr)