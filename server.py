import os
import socket 
from threading import Thread

# server address and port
HOST = '127.0.0.1'
PORT = 8820

# the directory in which the files would be stored
file_directory = 'C:\\Documents\\file_directory'
if not os.path.exists(file_directory):
    try:
        os.makedirs(file_directory)
        print(f"[INFO] Directory created: {file_directory}")
    except Exception as e:
        print(f"[ERROR] Failed to create directory: {e}")

# socket object
server = socket.socket()
server.bind((HOST, PORT))

def handle_client(client_socket, client_address):
    file_name = client_socket.recv(1024).decode()
    file_content = client_socket.recv(1024)

    with open(f"{file_directory}\\{file_name}", 'wb') as file:
        file.write(file_content)
    client_socket.close()

def start_server():
    server.listen()
    print("[RUNNING]")
    client_socket, client_address = server.accept()
    print(f"[HANDLING] {client_address}")
    handle_client(client_socket, client_address)

running = True
while running:
    start_server()
    
    




