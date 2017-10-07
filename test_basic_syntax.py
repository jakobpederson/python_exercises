import os
import unittest

from basic_syntax import sum_digits, most_common_word


class BasicSyntaxOneTest(unittest.TestCase):

    def test_sum_digits_returns_correct_answer(self):
        self.assertEqual(0, sum_digits(0))
        self.assertEqual(1, sum_digits(1))
        self.assertEqual(1, sum_digits(10))
        self.assertEqual(1, sum_digits(100))
        self.assertEqual(2, sum_digits(20))
        self.assertEqual(3, sum_digits(12))
        self.assertEqual(17, sum_digits(98))
        self.assertEqual(17, sum_digits(89))


class BasicSyntaxTwoTest(unittest.TestCase):


    def setUp(self):
        self.FILES = {
        "test_1.txt": "duck duck duck goose",
        "test_2.txt": "cat cat",
        "test_3.txt": " "
        }
        self.delete_if_exists()
        for path, data in self.FILES.items():
            with open(path, 'w') as f:
                f.write(data)

    def tearDown(self):
        self.delete_if_exists()

    def delete_if_exists(self):
        for path in self.FILES.keys():
            self.delete_or_pass(path)

    def delete_or_pass(self, path):
        try:
            os.remove(path)
        except OSError:
            pass

    def test_gets_most_common_word_and_count(self):
        self.assertEqual(('duck', 3), most_common_word("test_1.txt"))
        self.assertEqual(('cat', 2), most_common_word("test_2.txt"))
        self.assertEqual(("No words"), most_common_word("test_3.txt"))
