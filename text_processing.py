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

HEADER = (
    'interface',
    'inet',
    'status'
)


def get_data(lines):
    data = split_out_data(lines)
    return fill_gaps(data)

def get_data(lines):
    data = []
    count = 0
    for line in lines:
        route = router(line)
        if route:
            count, data = OPTIONS[route](data, line, count)
    result = []
    tags = set([x[0] for x in data])
    for tag in tags:
        result.append([x[1] for x in data if x[0] == tag])
    result.insert(0, HEADER)
    return result

def router(line):
    if len(line.split(' flags')) > 1:
        return 'flags'
    if len(line.split('status:')) > 1:
        return 'status'
    if len(line.split('inet ')) > 1:
        return 'inet'
    return None

def add_flag(data, line, count):
    count += 1
    data.append((count, line.split(':')[0].strip(' ')))
    return count, data

def add_status(data, line, count):
    status = line.strip('\n').strip(' ').split('status: ')[1]
    data.append((count, status))
    return count, data

def add_inet(data, line, count):
    stripped = line.strip('\n').strip(' ')
    data.append((count, stripped.split(' netmask')[0][5:]))
    return count, data

OPTIONS = {
    'flags': add_flag,
    'status': add_status,
    'inet': add_inet,
}
