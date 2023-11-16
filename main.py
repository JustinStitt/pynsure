import pynsure


@pynsure.validate()
def add_two(a: pynsure.Unsigned, b: pynsure.Negative) -> pynsure.Unsigned:
    return a + b


pynsure.foo(2, 3)

add_two(23, -3)
