def validate_depth(depth: int) -> int:
    if depth is None:
        return 1

    if depth < 0:
        return 0

    if depth > 5:
        return 5

    return depth