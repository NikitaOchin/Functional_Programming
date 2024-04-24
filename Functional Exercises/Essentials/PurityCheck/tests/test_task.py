import unittest

from Essentials.PurityCheck.task import is_pure, Integer


class TestCase(unittest.TestCase):
    def test_ensures_state_modifying_function_is_detected(self):
        def non_pure(i: Integer) -> Integer:
            i.value += 1
            return i

        self.assertFalse(is_pure(non_pure), "Expected given function is not pure")

    def test_ensures_changing_state_relying_function_is_detected(self):
        global cache
        cache = None

        def non_pure(i: Integer) -> Integer:
            global cache
            next_el = Integer(i.value + 1)
            if cache is None:
                cache = next_el

            return cache

        self.assertFalse(is_pure(non_pure), "Expected given function is not pure")

    def test_ensures_pure_function_is_detected(self):
        self.assertTrue(is_pure(lambda i: Integer(i.value + 1)), "Expected given function is pure")
