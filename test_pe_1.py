import unittest

from pe_1 import sum_digits


class PythonExerciseOneTest(unittest.TestCase):

    def test_sum_digits_returns_correct_answer(self):
        self.assertEqual(0, sum_digits(0))
        self.assertEqual(1, sum_digits(1))
        self.assertEqual(1, sum_digits(10))
        self.assertEqual(1, sum_digits(100))
        self.assertEqual(2, sum_digits(20))
        self.assertEqual(3, sum_digits(12))
        self.assertEqual(17, sum_digits(98))
        self.assertEqual(17, sum_digits(89))
