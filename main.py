import pynsure


@pynsure.validate()
def add_two(a: pynsure.Unsigned, b: pynsure.Negative) -> pynsure.Unsigned:
    return a + b


add_two(23, -4)
