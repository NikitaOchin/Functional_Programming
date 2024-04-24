from typing import Callable

from Essentials.Factorial.tail_recursion import tail_call_optimized


@tail_call_optimized
def factorial_impl() -> Callable[[int], int]:
    def func(n):
        return 1 if n <= 1 else n * func(n - 1)

    return func
