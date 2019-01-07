import socket, select, sys, os, subprocess, threading

servers = [ 'ctf.q3msk.ru', 'meat.q3msk.ru', 'q3msk.ru:7790', 'q3msk.ru', 'q3msk.ru:27961', 'q3msk.ru:27962', 'q3msk.ru:27963', 'q3msk.ru:27964' ]

class run_thread(threading.Thread):
   
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
    def run(self):
               
        #log.debug('####### thread number: ' + str(self.counter) + ' , thread mac: ' + self.mac + ' ######\n')
        result = run_quake(self.server)
        #log("%s zakonczony %s" % (self.counter, result))
        #log.debug('####### thread number: #####')
        #log.debug(str(self.counter))
        #log.debug(self.mac)

#def set_server():

#def get_servers():
def run_quake(server):
    os.chdir('e:\g\q3')
    #subprocess.call(['cd e:\g\q3'])
    subprocess.Popen('quake3.exe +connect ctf.q3msk.ru')
    #subprocess.Popen('cd E:\g\q3\\')
    #subprocess.Popen('E:')
    #subprocess.Popen(['e:\g\q3\quake3.exe +connect ctf.q3msk.ru'])
def set_info_query(base):
    info = base
    info += b'getinfo xxx'
    return info
def set_status_query(base):
    status = base
    status += b'getstatus xxx'
    return status
def parse_respond(buf):
    print('buf: ', buf)

def check_port(servers):
    for server in servers:
        if any(":" in s for s in server):
            port_index = server.find(':')
            port = server[port_index : len(server)]
            port = port.strip(':')
            server = server[0 : port_index]
        else:
            port = 27960
        scan_servers(server, port, set_info_query(base))
def scan_servers(server, port, info):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(port)
    print('server: ', server,  'port: ', port)
    sock.connect((server, port))
    if (sock.sendto(info, (server, port)) == 1):
        print('sendto error')

    while (True):
        buf = ''
        timeout = 1
        r,w,e = select.select([sock], [], [], timeout)
        if sock in r:
            buf = sock.recvfrom(1024)
            parse_respond(buf)
            break
        else:
            print('no data')
    
    if (sock.sendto(info, (server, port)) == 1):
        print('sendto error')
def menu():
    while True:
        print('\n         Quake 3 scanner\n')
        print('select option:           \n')
        print('(1) print servers')
        print('(2) add server')
        print('(3) remove server')
        print('(4) scan')
        print('(5) connect')
        print('(q) quit')
        user_input = input()
        if user_input == 'q':
            break
        elif user_input == '4':
            check_port(servers)
            os.system("PAUSE")
        elif user_input == '5':
            #create thread here, change folder and then run q3
            server = 'asd'
            run_thread(server).start()
            #subprocess.Popen('E:\g\q3\quake3.exe')
        else:
            continue

base= b'\xFF\xFF\xFF\xFF'
menu()



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
