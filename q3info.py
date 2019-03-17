import socket, select, sys, os, subprocess, threading, wmi

#servers = [ 'ctf.q3msk.ru', 'meat.q3msk.ru', 'q3msk.ru:7790', 'q3msk.ru', 'q3msk.ru:27961', 'q3msk.ru:27962', 'q3msk.ru:27963', 'q3msk.ru:27964' ]


def check_q3process():
    c = wmi.WMI()
    for process in c.Win32_Process():
        if(process.Name == "quake3.exe"):
            return process
    return False

def kill_q3process(q3process):
    q3process.Terminate()

class run_thread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
    def run(self):
        result = run_quake(self.server)

def run_quake(server):
    script_dir = os.getcwd()
    os.chdir('d:\g\q3')
    q = 'quake3.exe +connect ' + server
    subprocess.Popen(q)
    os.chdir(script_dir)

def connect(server_dict):
    while True:
        server_count = show_servers(server_dict)
        choice = input('\nenter server number to connect or (c) to cancel:\n ')
        if choice == 'c':
            break
        else:
            if validate_choice(choice, server_count):
                server = server_dict[int(choice)]
                q3process = check_q3process()
                if(q3process):
                    kill_q3process(q3process)
                run_thread(server).start()
                break

def set_info_query(base):
    info = base
    info += b'getinfo xxx'
    return info

def set_status_query(base):
    status = base
    status += b'getstatus xxx'
    return status

def make_servers_dict():
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
        return server_dict

def show_servers(server_dict):
    print('server list contains:\n')
    servers_count = len(server_dict)
    #from 1 to servers_count, print number and dict value
    for server in range(1, servers_count+1):
        print(server, server_dict[server])
    return servers_count

def count_servers(server_dict):
    servers_count = len(server_dict)
    return servers_count

def add_server():
    get_servers = open(servers_file, 'a')
    #print('enter server address or address:port')
    server_from_user = input('enter server address or address:port\n: ')
    if server_from_user.find(':') == -1:
        print('port not given. default added')
        server_from_user = server_from_user + ':27960'
        print('server with port: ', server_from_user)
    get_servers.write(server_from_user + '\n')
    get_servers.close()
    return show_servers(make_servers_dict())

def validate_choice(choice, servers_count):
    if choice.isdigit():
        if int(choice) <= servers_count and int(choice) > 0:
            return True
        else:
            print('wrong number\n')
            return False
    else:
        print('wrong number\n')
        return False

def remove_server(server_dict):
    while True:
        servers_count = show_servers(server_dict)
        choice = input('\nenter server number to remove or (c) to cancel:\n ')
        if choice == 'c':
            break
        else:
            if validate_choice(choice, servers_count):
                file = open(servers_file, 'r')
                server_lines = file.readlines()
                file.close()
                file = open(servers_file, 'w')
                for line in server_lines:
                    if line != str(server_dict[int(choice)] +'\n'):
                        file.write(line)
                file.close()
                print('server removed')
                return show_servers(make_servers_dict())

def parse_respond(buf, server_number):
    #print('buf: ', buf)
    hostname_start = buf.find('hostname')
    hostname_end = buf.find('protocol')
    hostname = buf[hostname_start+20 : hostname_end-10]
    hum_players_start = buf.find('g_humanplayers')
    hum_players = buf[hum_players_start : ]
    hum_players_start = hum_players.find('g_humanplayers')
    hum_players_end = hum_players.find('clients')
    mapname_start = buf.find('mapname')
    mapname = buf[mapname_start+9 : hostname_start-2]
    hum_players = hum_players[hum_players_start+16 : hum_players_end-2]
    print('{3}: hostname: {0}  players: {1}  map: {2}'.format(hostname, hum_players, mapname, server_number))

def scan_servers(server_dict, info):
    #print('SERVER: ' , server)
    for server in range(1, count_servers(server_dict)+1):
        if any(":" in s for s in server_dict[server]):
            server_number = server
            port_index =server_dict[server].find(':')
            port = server_dict[server][port_index : len(server_dict[server])]
            port = port.strip(':')
            server = server_dict[server][0 : port_index]
        #TODO:
        #else:
            #tu jest ryzyko, ze jesli ktos doda z palca cos to pliku i nie bedzie tam : to sie zesra
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = int(port)
        sock.connect((server, port))
        if (sock.sendto(info, (server, port)) == 1):
            print('sendto error')
        while (True):
            buf = ''
            timeout = 1
            r,w,e = select.select([sock], [], [], timeout)
            if sock in r:
                buf = sock.recvfrom(1024)
                parse_respond(str(buf), server_number)
                break
            else:
                print('no data')
                break
        if (sock.sendto(info, (server, port)) == 1):
            print('sendto error')
    #os.system("PAUSE")
    #TODO: po udanym skanowaniu zatrzymaj os.system("PAUSE")

def manage_choice(choice):
    if choice == '1':
        scan_servers(make_servers_dict(), set_info_query(base))
    elif choice == '2':
        connect(make_servers_dict())        
    elif choice == '3':
        show_servers(make_servers_dict())
    elif choice == '4':
        add_server()
    elif choice == '5':
        remove_server(make_servers_dict())
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
        user_input = input(': ')
        if user_input == 'q':
            break
        else:
            manage_choice(user_input)
        
base= b'\xFF\xFF\xFF\xFF'
servers_file = 'server_list.txt'
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
