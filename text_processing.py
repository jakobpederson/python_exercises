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
    result = {get_just_interface(line): get_data(lines) for line in lines if not_interface(line)}
    result.pop("blank", None)
    print(result)

def get_just_interface(line):
    for value in line.split(':'):
        if value.startswith(' flags'):
            return line.split(':')[0]
    return "blank"

def get_data(lines):
    interface = []
    inet = []
    activity = []
    x = []
    for line in lines:
        count = True
        if len(line.split(' flags')) > 1:
            interface.append(line.split(' flags')[0])
            x.append(line.split(':')[0])
        if len(line.split('inet ')) > 1:
            inet.append(line.split('inet ')[1])
            x.append(line[5:].strip('\n'))
        if len(line.split('status:')) > 1:
            activity.append(line.split('status:'))
            x.append(line)
    for y in x[1::3]:
        if not y.startswith('status:'):
            ind = x.index(y)
            x.insert(ind + 1, '0')
    data = [x[y:y+3] for y in range(0, len(x), 3)]
    return data

    # print(interface)
    # print(inet)
    # print(activity)

    # y = data.split('inet ')
    # print('inet\n', y)
    # z = data.split('status')
    # print('status\n', z)

    # all_results = []
    # for x in (line.split(' flag') for line in lines):
    #     if len(x) > 1:
    #         result.append(x[0])
    #     elif x[0].startswith('inet '):
    #         result.append(x[0])
    #     elif x[0].startswith('status'):
    #         result.append(x[0])
    # if len(result) < 3:
    #     result.append(0)
    # return result




    # result = {
    #     line.split(':')[0]: [
    #         line for line in not_interface(lines)
    #         ] for line in lines if len(line.split(':')) > 1 and line.split(':')[1].startswith(' flags')}
    # print(result)
    # return result

def not_interface(line):
    data = line.split(':')
    if len(data) is 1 or not data[1].startswith(' flags'):
        yield line

    # result = []
    # status = False
    # for line in lines:
    #     if line.startswith('status:'):
    #         result.append(line[7:].replace('\n', ''))
    # return result

