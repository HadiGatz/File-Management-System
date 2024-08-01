import os
import socket 
from threading import Thread

# server address and port
HOST = '127.0.0.1'
PORT = 8820

# the directory in which the files would be stored
file_directory = 'C:\Documents\\file_directory'
if not os.path.exists(file_directory):
    os.makedirs(file_directory)

# socket object
server = socket.socket()
server.bind((HOST, PORT))

def handle_client(client_socket, client_address):
    file_name = client_socket.recv().decode()
    file_content = client_socket.recv()

    with open(f"{file_directory}\{file_name}", 'wb') as file:
        file.write(file_content)
    client_socket.close()

def start_server():
    server.listen()
    print("[RUNNING]")
    client_socket, client_address = server.accept()
    print(f"[HANDLING] {client_address}")
    handle_client(client_socket, client_address)
    




