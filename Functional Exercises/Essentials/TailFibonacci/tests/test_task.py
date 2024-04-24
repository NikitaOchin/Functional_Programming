import sys
import unittest
from random import randint

from Essentials.TailFibonacci.task import fibonacci_impl


class TestCase(unittest.TestCase):
    def test_fib_1(self):
        self.assertEqual(fibonacci_impl()(1), 1, msg="fib of 1 should be 1")

    def test_fib_0(self):
        self.assertEqual(fibonacci_impl()(0), 0, msg="fib of 0 should be 0")

    def test_fib_max(self):
        fibonacci_impl()(sys.getrecursionlimit() + 2)

    def test_fib_rnd(self):
        for i in range(0, 50):
            rnd = randint(1, 5000)
            prev = fibonacci_impl()(rnd - 1)
            current = fibonacci_impl()(rnd)
            next_el = fibonacci_impl()(rnd + 1)
            self.assertEqual(prev + current, next_el, msg=f"fib of {next_el} should be {prev} + {current}")
