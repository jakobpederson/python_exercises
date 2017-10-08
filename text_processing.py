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
    data = split_out_data(lines)
    return fill_gaps(data)

def split_out_data(lines):
    data = []
    for line in lines:
        if len(line.split(' flags')) > 1:
            data.append(line.split(':')[0] + '|')
        if len(line.split('inet ')) > 1:
            data.append(line[5:].strip('\n') + '||')
        if len(line.split('status:')) > 1:
            data.append(line + '|||')
    for i in range(len(data)):
        print(data[i])
        if data[i].endswith('|'):
            if not data[i+1].endswith('||') and not data[i + 1] == '0':
                data.insert(i + 1, '0')
        if data[i].endswith('||'):
            if not data[i+1].endswith('|||') and not data[i + 1] == '0':
                data.insert(i + 1, '0')
    print(data)
    return data


def fill_gaps(data):
    if len(data) < 2:
        data.append('0')
    if len(data) < 3:
        data.append('0')
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
