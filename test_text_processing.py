import os
import unittest
from collections import namedtuple

import text_processing


Stats = namedtuple("Stats", ["interface", "inet", "status"])


class TextProcessingTest(unittest.TestCase):

    def setUp(self):
        self.FILES = {
            "test_1.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\ngif0: flags=9<up>mtu\noptions=12\ninet 9101\nstatus:active",
            "test_2.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\np2p0: flags=9<up>mtu\noptions=12\ninet 9101",
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

    def test_get_data(self):
        lines = self.get_lines('test_1.txt')
        result = text_processing.get_data(lines)
        expected = [
            ['lo0', '1234'],
            ['gif0', '9101', 'status:active'],
        ]
        self.assertCountEqual(result, expected)

    def test_longer_file(self):
        lines = self.get_lines('test_1.txt')
        lines += self.get_lines('test_2.txt')
        result = text_processing.get_data(lines)
        expected = [
            ['lo0', '1234'],
            ['gif0', '9101', 'status:active'],
            ['lo0', '1234'],
            ['p2p0', '9101'],
        ]
        self.assertCountEqual(result, expected)

    def get_lines(self, file_name):
        with open(file_name, 'r') as f:
            return f.readlines()
