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

def get_data(lines):
    x = []
    for line in lines:
        count = True
        if len(line.split(' flags')) > 1:
            x.append(line.split(':')[0])
        if len(line.split('inet ')) > 1:
            x.append(line[5:].strip('\n'))
        if len(line.split('status:')) > 1:
            x.append(line)
    if len(x) < 3:
        x.append('0')
    return get_activity(x)


def get_activity(data):
    if len(data) > 3 and len(data) % 3 != 0:
        for y in data[1::3]:
            if not y.startswith('status:'):
                ind = data.index(y)
                data.insert(ind + 1, '0')
        result = [data[y:y+3] for y in range(0, len(data), 3)]
        for lst in result:
            if len(lst) < 3:
                lst.append('0')
        return result
    return [data]
