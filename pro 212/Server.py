import socket
from  threading import Thread
import time
import os


#For FTP Server
# Student Boilerlate Code Start
#pip install pyftpdlib < this should be installed
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
# Student Boilerlate Code End


IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096
clients = {}

#Creating shared_files directory on server
is_dir_exists = os.path.isdir('shared_files')
print(is_dir_exists)
if(not is_dir_exists):
    os.makedirs('shared_files')

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"         : client,
                "address"        : addr,
                "connected_with" : "",
                "file_name"      : "",
                "file_size"      : 4096
            }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()
        
def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    # Listening incomming connections
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


#------ Student Activity 1 Start---------------
def ftp():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd","lftpd",".",perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer((IP_ADDRESS,21),handler)
    ftp_server.serve_forever()

setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()


ftp_thread = Thread(target=ftp)               #receiving multiple messages
ftp_thread.start()
#------ Student Activity 1 End---------------