import unittest
from pynsure import validate, Unsigned, UnsignedEven, Negative, ValidationError


class TestValidate(unittest.TestCase):
    def test_valid01(self):
        @validate()
        def add_two(a: Unsigned, b: Unsigned) -> Unsigned:
            return a + b

        add_two(4, 5)

    def test_valid02(self):
        @validate(cache=True, strict=False)
        def add_two(a: Unsigned, b: UnsignedEven) -> Negative:
            return a + b - 10**4

        add_two(4, 6)

    def test_valid03(self):
        @validate(strict=True)
        def add_two(a: Negative, b: Negative) -> UnsignedEven:
            return a + b + 24

        add_two(-6, -6)

    def test_valid04(self):
        @validate()
        def add_three(a: int, b: int, c=2):
            return a + b + c

        add_three(5, b=4)

    def test_valid05(self):
        @validate(cache=True)
        def add_two(a: int = 5, b: Unsigned = 2) -> Unsigned:
            return a + b

        add_two()

    def test_valid06(self):
        @validate(cache=True)
        def add_two(a: int = 5, b: Unsigned = 2) -> int:
            return a + b

        add_two()

    def test_invalid01(self):
        with self.assertRaises(ValidationError):

            @validate()
            def add_two(a: int = 5, b: Unsigned = -2) -> Unsigned:
                return a + b

            add_two()

    def test_invalid02(self):
        with self.assertRaises(ValidationError):

            @validate()
            def add_two(a: int, b: int) -> UnsignedEven:
                return a + b

            add_two(4, 5)
