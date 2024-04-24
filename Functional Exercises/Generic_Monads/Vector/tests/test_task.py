import unittest

from Generic_Monads.Vector.task import do_math, Vector


# todo: replace this with an actual test
class TestCase(unittest.TestCase):
    def test_1(self):
        result = do_math(Vector(1, 2, 3), Vector(3, 2, 1), Vector(3, 3, 3))
        self.assertEqual(result, Vector(1, 1, 1), f"{result} should be equal to {Vector(1, 1, 1)}")

    def test_2(self):
        result = Vector(1, 2, 3).transform(lambda v: Vector(1, 1, 1),
                                           lambda v: Vector(2, 2, 2),
                                           lambda v: Vector(3, 3, 3))
        self.assertEqual(result, Vector(3, 3, 3), f"{result} should be equal to {Vector(3, 3, 3)}")

    def test_3(self):
        result = Vector(1, 2, 3).transform(lambda v: Vector(v[0] + 1, v[1] + 1, v[2] + 1))
        self.assertEqual(result, Vector(2, 3, 4), f"{result} should be equal to {Vector(2, 3, 4)}")
