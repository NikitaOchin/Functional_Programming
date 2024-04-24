import math


def is_prime(n: int) -> bool:
    return not (
            n % 2 == 0
            or
            any(
                [
                    n % x == 0
                    and
                    n != x
                    for x in range(3, int(math.sqrt(n)) + 2, 2)
                ]
            )
    )
