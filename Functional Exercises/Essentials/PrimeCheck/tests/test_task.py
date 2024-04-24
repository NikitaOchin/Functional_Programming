import unittest

from Essentials.PrimeCheck.task import is_prime


# todo: replace this with an actual test
class TestCase(unittest.TestCase):
    def test_ensures_numbers_are_prime(self):
        for num in [3, 7, 11, 773, 507961]:
            self.assertTrue(is_prime(num), msg=f"Expected ${num} to be prime")

    def test_ensures_nums_are_not_prime(self):
        for num in [15, 507962]:
            self.assertFalse(is_prime(num), msg=f"Expected ${num} not to be prime")

    def test_ensures_any_pow_of_2_is_no_prime(self):
        for num in range(2, 64, 2):
            value = pow(2, num)
            self.assertFalse(is_prime(value), msg=f"Expected ${value} not to be prime")
