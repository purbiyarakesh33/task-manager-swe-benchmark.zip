def validate_title(title: str) -> str:
    normalized = " ".join(title.split())

    if not normalized:
        raise ValueError("title must not be empty")

    if len(normalized) > 100:
        raise ValueError("title must be at most 100 characters")

    return normalized
