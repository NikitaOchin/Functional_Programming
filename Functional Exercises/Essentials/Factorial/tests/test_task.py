import unittest
from random import randint

from Essentials.Factorial.task import factorial_impl


# todo: replace this with an actual test
class TestCase(unittest.TestCase):
    def test_f_0(self):
        self.assertEqual(factorial_impl()(0), 1, msg="factorial of 0 should be 1")

    def test_f_1(self):
        self.assertEqual(factorial_impl()(1), 1, msg="factorial of 1 should be 1")

    def test_f_5(self):
        self.assertEqual(factorial_impl()(5), 120, msg="factorial of 5 should be 120")

    def test_f_rnd(self):
        for i in range(0, 10):
            factorial = factorial_impl()
            rnd = randint(1, 500)
            res_rnd = factorial(rnd)
            res_prev_rnd = factorial(rnd - 1)
            res_f = res_rnd / res_prev_rnd

            self.assertEqual(res_f, rnd, msg=f"Expected factorial({rnd}) / factorial({rnd - 1}) is {rnd} but got {res_rnd} / {res_prev_rnd} is {res_f}")
