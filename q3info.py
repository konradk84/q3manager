import socket, select, sys, os, subprocess, threading

from querys import set_info_query, set_status_query

#servers = [ 'ctf.q3msk.ru', 'meat.q3msk.ru', 'q3msk.ru:7790', 'q3msk.ru', 'q3msk.ru:27961', 'q3msk.ru:27962', 'q3msk.ru:27963', 'q3msk.ru:27964' ]

class run_thread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
    def run(self):
        result = run_quake(self.server)

def run_quake(server):
    #os.chdir('e:\g\q3')
    #subprocess.call(['cd e:\g\q3'])
    q = 'quake3.exe +connect ctf.q3msk.ru'
    #subprocess.Popen(q)
    print('working')

def make_servers_dic():
    if not os.path.isfile(servers_file):
        print('there is no servers yet')
    else:
        number = 0
        server_dict ={}
        get_servers = open(servers_file, 'r')
        if not get_servers:
            print('not able to open file')
        while True:
            server_line = get_servers.readline()
            server_line = server_line.strip('\n')
            number = number + 1
            if server_line == '':
                get_servers.close()
                return server_dict
            server_dict[number] = server_line
            #print("mamy: ", server_dict.values())

def show_servers(server_dict):
    servers_count = len(server_dict)
    #print("mamyw show servers: ", server_dict.values(), server_dict.keys())
    #from 1 to servers_count, print number and dict value
    for server in range(1, servers_count+1):
        print(server, server_dict[server])
    return servers_count

def add_server():
    get_servers = open(servers_file, 'a')
    print('enter server address or address:port')
    server_from_user = input()
    if server_from_user.find(':') == -1:
        print('port not given. default added')
        server_from_user = server_from_user + ':27960'
        print('server with port: ', server_from_user)
    get_servers.write(server_from_user + '\n')
    get_servers.close()

def remove_server(server_dict):
    while True:
        print('server list contains:\n')
        servers_count = show_servers(server_dict)
        print('\nenter server number to remove or (e) to exit')
        choice = input()
        print('jest?: ', choice.isdigit())
        if choice == 'e':
            break
        elif choice.isdigit():
            if int(choice) < servers_count or int(choice) > 0:
                print('otiweramy')
                file = open(servers_file, 'r')
                server_lines = file.readlines()
                file.close()
                file = open(servers_file, 'w')
                for line in server_lines:
                    if line != str(server_dict[int(choice)] +'\n'):
                        file.write(line)
                        #print('asd: ', line)
                        #print(server_dict[int(choice)])
                        #print('linia: ', len(line), type(line))
                        #print('warosc: ', len(server_dict[int(choice)]), type(server_dict[int(choice)]))
                file.close()
                break
            else:
                print('wrong number\n')    
        else:
            print('wrong number\n')
            continue
        #servers_count = len(server_dict)
        #print(type(servers_count), type(choice))

def parse_respond(buf):
    print('buf: ', buf)

def check_port(servers):
    #for server in servers:
    '''
    if any(":" in s for s in server):
        port_index = server.find(':')
        port = server[port_index : len(server)]
        port = port.strip(':')
        server = server[0 : port_index]
        return server
    else:
        port = 27960
        scan_servers(server, port, set_info_query(base))
        '''
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
def manage_choice(choice):
    if choice == '1':
        check_port(servers)
        os.system("PAUSE")
    elif choice == '2':
        server = 'asd'
        run_thread(server).start()
    elif choice == '3':
        show_servers(server_dict)
    elif choice == '4':
        add_server()
    elif choice == '5':
        remove_server(server_dict)
    else:
        print('wrong choice')

def menu():
    while True:
        print('\n         Quake 3 scanner\n')
        print('select option:           \n')
        print('(1) scan')
        print('(2) connect')
        print('(3) show servers')
        print('(4) add server')
        print('(5) remove server')
        print('(q) quit')
        user_input = input()
        if user_input == 'q':
            break
        else:
            manage_choice(user_input)
        
base= b'\xFF\xFF\xFF\xFF'
servers_file = 'server_list.txt'
server_dict = make_servers_dic()
#print(server_dict.keys())
#print(server_dict.values())
#print(server_dict[3])
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
