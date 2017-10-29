import os
import unittest
from collections import namedtuple

import text_processing


Stats = namedtuple("Stats", ["interface", "inet", "status"])


class TextProcessingTest(unittest.TestCase):

    def setUp(self):
        self.FILES = {
            "test_1.txt": "lo0: flags=9<up>mtu\noptions=12::\ninet 1234\nstatus:active",
            "test_2.txt": "en0: flags=9<up>mtu\noptions=12\ninet 5678\n",
            "test_3.txt": "en1'': flags=9<up>mtu\noptions=12\n",
            "test_4.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\ngif0: flags=9<up>mtu\noptions=12\ninet 9101\nstatus:active",
            "test_5.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\np2p0: flags=9<up>mtu\noptions=12\ninet 9101",
            "test_6.txt": "en0"": flags=9<up>mtu\noptions=12\nlo0: flags=9<up>mtu\noptions=12\ninet 9101\nlo0: flags=9<up>mtu\noptions=12::\ninet 1234\nstatus:active\nlo0: flags=9<up>mtu\noptions=12::\ninet 1234\nstatus:active"
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
        lines = self.get_lines('test_4.txt')
        result = text_processing.get_data(lines)
        expected = [
            "lo0",
            "1234",
            "gif0",
            "9101",
            "status:active"
        ]
        self.assertCountEqual(expected, result)
        lines = self.get_lines('test_5.txt')
        result = text_processing.get_data(lines)
        expected = [
            "lo0",
            "1234",
            "p2p0",
            "9101",
        ]
        self.assertCountEqual(expected, result)

    def test_x(self):
        lines = self.get_lines('test_4.txt')
        lines += self.get_lines('test_5.txt')
        data = text_processing.get_data(lines)
        new_data = data
        result = []
        z = []
        g = text_processing.gen_interface(data)
        while True:
            try:
                x = next(g)
                y = next(g)
                z.append(x)
                z.append(y)
                a = set(z)
                    # print(ii)

            except StopIteration:
                break
        for ii in range(len(set(z))):
            if ii + 1 < 4:
                print(list(a)[ii])
                result.append(data[list(a)[ii]:list(a)[ii+1]])
        print(result)
        expected = [
            [
                "lo0",
                "1234",
                "gif0",
                "9101",
                "status:active"
            ],
        ]
        self.fail('x')
        self.assertCountEqual(formatted_data, expected)

    def get_lines(self, file_name):
        with open(file_name, 'r') as f:
            return f.readlines()
