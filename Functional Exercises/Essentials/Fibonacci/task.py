from typing import Callable


def fibonacci_impl() -> Callable[[int], int]:
    def func(n):
        return n if n <= 1 else func(n - 2) + func(n - 1)

    return func