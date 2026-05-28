def detect_cycle(department, new_parent):
    current = new_parent

    while current:
        if current.id == department.id:
            return True
        current = current.parent

    return False