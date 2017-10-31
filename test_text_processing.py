import os
import unittest
from collections import namedtuple

import text_processing


Stats = namedtuple("Stats", ["interface", "inet", "status"])


class TextProcessingTest(unittest.TestCase):

    def setUp(self):
        self.FILES = {
            "test_1.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\ngif0: flags=9<up>mtu\noptions=12\ninet 9101\nautoselect status: active",
            "test_2.txt": "lo0: flags=9<up>mtu\noptions=12\ninet 1234\np2p0: flags=9<up>mtu\noptions=12\ninet 9101",
            "test_3.txt": "lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 1638\noptions=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>\n\
                inet 127.0.0.1 netmask 0xff000000\n\
                inet6 ::1 prefixlen 128\n\
                inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1\n\
                nd6 options=201<PERFORMNUD,DAD>\n\
                gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280\n\
                en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500\n\
                ether f4:0f:24:29:df:4d\n\
                inet6 fe80::1cb5:1689:1826:cc7b%en0 prefixlen 64 secured scopeid 0x4\n\
                inet 10.176.85.19 netmask 0xffffff00 broadcast 10.176.85.255\n\
                nd6 options=201<PERFORMNUD,DAD>\n\
                media: autoselect status: active\n\
                en1: flags=963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX> mtu 1500\n\
                options=60<TSO4,TSO6>\n\
                ether 06:00:58:62:a3:00\n\
                media: autoselect <full-duplex>\n\
                status: inactive\n\
                p2p0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 2304\n\
                ether 06:0f:24:29:df:4d\n\
                media: autoselect\n\
                status: inactive\n"\
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
            ('interface', 'inet', 'status'),
            ['lo0', '1234'],
            ['gif0', '9101', 'active'],
        ]
        self.assertCountEqual(result, expected)

    def test_longer_file(self):
        lines = self.get_lines('test_1.txt')
        lines += self.get_lines('test_2.txt')
        result = text_processing.get_data(lines)
        print(result)
        expected = [
            ('interface', 'inet', 'status'),
            ['lo0', '1234'],
            ['gif0', '9101', 'active'],
            ['lo0', '1234'],
            ['p2p0', '9101'],
        ]
        self.assertCountEqual(result, expected)

    def test_actual_target_data(self):
        lines = self.get_lines('test_3.txt')
        result = text_processing.get_data(lines)
        print(result)
        expected = [
            ('interface', 'inet', 'status'),
            ['lo0', '127.0.0.1'],
            ['gif0'],
            ['en0', '10.176.85.19', 'active'],
            ['en1', 'inactive'],
            ['p2p0', 'inactive']
        ]
        self.assertCountEqual(result, expected)

    def get_lines(self, file_name):
        with open(file_name, 'r') as f:
            return f.readlines()
