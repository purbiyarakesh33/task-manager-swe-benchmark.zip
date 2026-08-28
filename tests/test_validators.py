import pytest

from task_manager.validators import validate_title


def test_title_is_trimmed_and_internal_whitespace_is_normalized():
    assert validate_title("  buy    milk  ") == "buy milk"


def test_empty_title_is_rejected():
    with pytest.raises(ValueError, match="must not be empty"):
        validate_title("   ")


def test_title_over_100_characters_is_rejected():
    with pytest.raises(ValueError, match="at most 100"):
        validate_title("x" * 101)
