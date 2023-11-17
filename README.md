# pynsure

Predicate-based runtime constraint validator for Python


## Check it out

Just use type hints and a decorator to verify parameter constraints at runtime.

```py
from pynsure import validate, Unsigned

@validate()
def add_two(a: Unsigned, b: int) -> int:
    return a + b

add_two(3, 4) # OK
add_two(-2, 4) # BAD
```

Make your own types using `typing.Annotated`!

```py
from pynsure import validate
from typing import Annotated

Odd = Annotated[int, (lambda _v: _v & 1 == 1, "{} must be odd but its value is {{}}")]

@validate()
def add_two(a: Odd, b: Odd):
    return a + b

add_two(3, 5) # OK
add_two(4, 5) # BAD
```

Note: `{}` is replaced with the parameter name and `{{}}` is replaced by the
parameter value automatically when a `ValidationError` is raised.

You can even specify multiple predicates for your Annotated types:

```py
from pynsure import validate
from typing import Annotated

PositiveAndOdd = Annotated[
    int,
    (lambda _v: _v & 1 == 1, "{} must be odd but its value is {{}}"),
    (lambda _v: _v > 0, "{} must be greater than 0 but its value is {{}}"),
]

@validate()
def add_two(a: PositiveAndOdd, b: PositiveAndOdd) -> int:
    return a + b

add_two(7, 9) # OK
add_two(-7, 9) # BAD
add_two(7, 8) # BAD
```

Only Annotated types following this form are validated:

`MyType = Annotated[<base_type>, (<predicate>, <message>), <...>]` where `...`
can be more predicate + message tuples


## "Why not use asserts?"

Valid point.

Basically, `pynsure` makes it easier for users of your functions to understand
the exact constraints surrounding a parameter (or return value). You can make
and document your constraints and have them runtime-validated in just a few
easy steps.

If my function expects four positive numbers, it's a whole lot easier to
annotate like this:

```py
@validate()
def add_four(a: Unsigned, b: Unsigned, c: Unsigned, d: Unsigned) -> Unsigned:
    return a + b + c + d
```

...than it is to do this:

```py
def add_four(a, b, c, d):
    assert isinstance(a, int) and a >= 0, "a should be greater than or equal to 0"
    assert isinstance(b, int) and b >= 0, "b should be greater than or equal to 0"
    assert isinstance(c, int) and c >= 0, "c should be greater than or equal to 0"
    assert isinstance(d, int) and d >= 0, "d should be greater than or equal to 0"
    return
```

...plus `pynsure` will validate return types and return value constraints at
runtime too! if `add_four()` doesn't return an integer greater than or equal to
0, a `ValidationError` will be raised.


## "Why not use pydantic"

Great point.

`pydantic` is awesome (and battle-tested) but is a bit clunky if you want to do
basic constraints and don't necessarily need giant serializable objects that
you can convert from json to a dict and a whole bunch of other fancy stuff.

You have a function that expects non-empty strings? `pynsure` makes this a
breeze. Let's compare:


#### Using pynsure
```py
from pynsure import validate
from typing import Annotated

NonEmptyStr = Annotated[str, (lambda _s: len(_s) > 0, "{} shouldn't be empty")]

@validate()
def format_name(first_name: NonEmptyStr, last_name: NonEmptyStr) -> NonEmptyStr:
    return f"{last_name}, {first_name}"

format_name(first_name="Bob", last_name="Smith")
```

#### Using pydantic
```py
from pydantic import BaseModel, constr

class NonEmptyStr(BaseModel):
    string: constr(min_length=1)

def format_name(first_name: NonEmptyStr, last_name: NonEmptyStr) -> str:
    return f"{last_name}, {first_name}"

format_name(first_name=NonEmptyStr(string="Bob"), last_name=NonEmptyStr(string="Smith"))

```

This is fine but a bit clunky having to fiddle around with BaseModels.
