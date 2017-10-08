'''
Given the following input:
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
	options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
	inet 127.0.0.1 netmask 0xff000000
	inet6 ::1 prefixlen 128
	inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1
	nd6 options=201<PERFORMNUD,DAD>
gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether f4:0f:24:29:df:4d
	inet6 fe80::1cb5:1689:1826:cc7b%en0 prefixlen 64 secured scopeid 0x4
	inet 10.176.85.19 netmask 0xffffff00 broadcast 10.176.85.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
en1: flags=963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX> mtu 1500
	options=60<TSO4,TSO6>
	ether 06:00:58:62:a3:00
	media: autoselect <full-duplex>
	status: inactive
p2p0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 2304
	ether 06:0f:24:29:df:4d
	media: autoselect
	status: inactive
Create a CSV file from the data as follows:

interface,inet,status
lo0,127.0.0.1,
gif0,,
en0,10.176.85.19,active
en1,,inactive
p2p0,,inactive
'''
from collections import namedtuple
Stats = namedtuple("Stats", ["interface", "inet", "status"])

def create_list(data):
    r = range(len(data))
    for i in data[2::3]:
        if i not in ('active', 'inactive'):
            data[i].insert(i, "None")
    return data

def get_network_stats(file_name):
    result = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            colon_split = line.split(':')
            for value in colon_split:
                if value.startswith(' flag'):
                    result.append(colon_split[0])
                if value.startswith('inet '):
                   result.append(value[5:].strip('\n'))
                if value.startswith('status'):
                    for value in colon_split:
                        if value in ('active', 'inactive'):
                            result.append(value)
    return create_list(result)

def get_interface(lines):
    result = []
    for line in lines:
        for value in line.split(':'):
            if value.startswith(' flag'):
                result.append(line.split(':')[0])
    return result

def get_inet(lines):
    result = []
    for line in lines:
        if "inet " in line:
            result.append(line[5:].replace('\n', ''))
    return result

def get_status(lines):
    result = []
    status = False
    for line in lines:
        if line.startswith('status:'):
            result.append(line[7:].replace('\n', ''))
    return result

