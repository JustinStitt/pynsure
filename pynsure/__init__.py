import inspect
import functools
from typing import Annotated

# TODO: support multiple predicates and messages
# probably go with a dict approach
# but also still support non-dict approach
Unsigned = Annotated[
    int,
    lambda V: V >= 0,
    "`{}` must be greater than or equal to 0 but it is equal to {{}}",
]

Negative = Annotated[
    int,
    lambda V: V < 0,
    "{} must be negative(i.e: < 0) but it is equal to {{}}",
]


class ValidationError(TypeError):
    ...


# TODO: consider kwargs and optionals and defaults and pretty much all edge cases
def validate(cache=False, strict=True):
    """
    Validate Annotated types supplied with predicates.

    Args:
        cache (bool) : Cache repeat calls, arguments must be hashable.
        strict (bool): Check exact origin types as well as predicates

    Returns:
        A wrapper function that performs the validation before calling the actual function.
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            full_arg_spec = inspect.getfullargspec(func)
            # print(full_arg_spec)
            annotations = full_arg_spec.annotations
            # print(f"{annotations=}")

            for _var, _type in annotations.items():
                if not hasattr(_type, "__metadata__"):
                    continue

                if _var == "return":  # check return type after we have result
                    continue

                arg = args[full_arg_spec.args.index(_var)]

                if strict and not isinstance(arg, _type.__origin__):
                    raise TypeError(
                        f"Expected {_var} to have origin type of {_type.__origin__} yet it's type is {type(arg)}"
                    )

                msg = ""
                for x in _type.__metadata__:
                    if isinstance(x, str):
                        msg = x
                        break

                msg = msg.replace("{{}}", f"{arg}").replace("{}", _var)

                for entry in _type.__metadata__:
                    if callable(entry) and not entry(arg):
                        raise ValidationError(msg)

            result = func(*args, **kwargs)
            return_annotation = annotations.get("return", None)
            if not return_annotation or not getattr(
                return_annotation, "__metadata__", None
            ):
                return result

            msg = ""
            for x in return_annotation.__metadata__:
                if isinstance(x, str):
                    msg = x.replace("{{}}", f"{result}").replace("{}", "return value")

            for entry in return_annotation.__metadata__:
                # TODO: better info about which return statement returned bad result
                # use inspect module
                if callable(entry) and not entry(result):
                    raise ValidationError(msg)

            return result

        if cache:
            return functools.cache(inner)
        return inner

    return wrapper
