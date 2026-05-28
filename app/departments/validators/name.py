def validate_department_name(name: str) -> str:
    if not name:
        raise ValueError("Name cannot be empty")

    cleaned = name.strip()

    if len(cleaned) < 1 or len(cleaned) > 200:
        raise ValueError("Name must be 1..200 characters")

    return cleaned