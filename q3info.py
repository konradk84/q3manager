import socket, select, sys

servers = [ 'ctf.q3msk.ru', 'meat.q3msk.ru', 'q3msk.ru:7790', 'q3msk.ru', 'q3msk.ru:27961', 'q3msk.ru:27962', 'q3msk.ru:27963', 'q3msk.ru:27964' ]




for server in servers:
    if any(":" in s for s in server):
        port_index = server.find(':')
        port = server[port_index : len(server)]
        port = port.strip(':')
        server = server[0 : port_index]
    else:
        port = 27960
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(port)
    print('server: ', server,  'port: ', port)
    sock.connect((server, port))
    info = b'\xFF\xFF\xFF\xFF'
    status = info
    info += b'getinfo xxx'
    status += b'getstatus xxx'

    #print('info: ', info)
    #print('status: ', status)
    buf = ''

    if (sock.sendto(info, (server, port)) == 1):
        print('sendto error')

    while (True):
        timeout = 1
        r,w,e = select.select([sock], [], [], timeout)
        if sock in r:
            buf = sock.recvfrom(1024)
            print('buf: ', buf)
            break
        else:
            print('no data')

    buf = ''
    if (sock.sendto(status, (server, port)) == 1):
        print('sendto error')

    ''' #extra data
    while (True):
        timeout = 1
        r,w,e = select.select([sock], [], [], timeout)
        if sock in r:
            buf = sock.recvfrom(1024)
            print('buf: ', buf)
            break
        else:
            print('no data')
    '''
#print('servers: , meat.q3msk.ru, ctf.q3msk.ru, q3msk.ru:7790, ffa.q3msk.ru, q3msk.ru')

#if len(sys.argv) < 2:
#    print(''', Too few arguments. Usage: q3info.py <address> optional <port>''')
#    exit()

#if len(sys.argv) == 3:
#    port = sys.argv[2]
#else:
#    port = 27960
#host = sys.argv[1]
