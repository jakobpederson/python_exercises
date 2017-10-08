import os
import unittest

import text_processing


class TextProcessingTest(unittest.TestCase):

    def setUp(self):
        self.FILES = {
        "test_1.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\nstatus:active",
        "test_2.txt": "ex0: flags=9<up>mtu\noptions=12\ninet 5678\n",
        "test_3.txt": "zo0o: flags=9<up>mtu\noptions=12\ninet 9101\nstatus:active",
        "test_4.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\nstatus:active\nzo0o: flags=9<up>mtu\noptions=12\ninet 9101\nstatus:active",
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

    def test_extracts_network_stats(self):
        result_1 = text_processing.get_network_stats("test_1.txt")
        # result_2 = text_processing.get_network_stats("test_2.txt")
        # result_3 = text_processing.get_network_stats("test_3.txt")
        # result_4 = text_processing.get_network_stats("test_4.txt")
        self.assertCountEqual([["lo0", "1234", "active"]], result_1)
        # self.assertCountEqual(["ex0", "5678", ""], result_2)
        # self.assertCountEqual(["zo0o", "9101", "active"], result_3)

        # self.assertCountEqual([
        #     ["lo0", "1234", "active"],
        #     ["zo0o", "9101", "active"]
        # ], result_4)
