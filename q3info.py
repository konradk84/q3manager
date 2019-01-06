import socket, select, sys


print('servers: \nmeat.q3msk.ru\nctf.q3msk.ru\nq3msk.ru:7790\nffa.q3msk.ru\nq3msk.ru')

if len(sys.argv) < 2:
    print('''\nToo few arguments. Usage: q3info.py <address> optional <port>''')
    exit()

if len(sys.argv) == 3:
    port = sys.argv[2]
else:
    port = 27960
host = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server = ('92.38.139.47', 27975)
print('server: ', host,  'port: ', port)
port = int(port)
s.connect((host, port))
info = b'\xFF\xFF\xFF\xFF'
status = info
info += b'getinfo xxx'
status += b'getstatus xxx'

print('info: ', info)
print('status: ', status)
buf = ''

if (s.sendto(info, (host, port)) == 1):
    print('sendto error')

while (True):
    timeout = 1
    r,w,e = select.select([s], [], [], timeout)
    if s in r:
        buf = s.recvfrom(1024)
        print('buf: ', buf)
        break
    else:
        print('no data')

buf = ''
if (s.sendto(status, (host, port)) == 1):
    print('sendto error')

while (True):
    timeout = 1
    r,w,e = select.select([s], [], [], timeout)
    if s in r:
        buf = s.recvfrom(1024)
        print('buf: ', buf)
        break
    else:
        print('no data')
    
