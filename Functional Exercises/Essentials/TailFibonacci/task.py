from typing import Callable

from Essentials.TailFibonacci.tail_recursion import tail_call_optimized

@tail_call_optimized
def fib_helper(step, depth, previous_num, num):
    if step == depth:
        return num
    else:
        fib_helper(step + 1, depth, num, num + previous_num)


def fibonacci_impl() -> Callable[[int], int]:
    return lambda x: x if x < 2 else fib_helper(1, x, 1, 1)
