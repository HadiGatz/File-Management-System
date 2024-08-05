import os
import socket 
from threading import Thread

# server address and port
HOST = '127.0.0.1'
PORT = 8820
list_of_files = []

# the directory in which the files would be stored
file_directory = 'C:\\Users\\User\\Documents\\file_directory'

if not os.path.exists(file_directory):
    try:
        os.makedirs(file_directory)
        print(f"[INFO] Directory created: {file_directory}")
    except Exception as e:
        print(f"[ERROR] Failed to create directory: {e}")

# socket object
server = socket.socket()
server.bind((HOST, PORT))

def handle_client_sending_file(client_socket, client_address):
    try:
        file_name_length = int.from_bytes(client_socket.recv(2), byteorder='big')
        print(file_name_length)
        file_name = client_socket.recv(file_name_length).decode(encoding='utf-8')
        print(file_name)
        list_of_files.append(file_name)
        file_path = os.path.join(file_directory, file_name)
        
        with open(file_path, 'wb') as file:
            while True:
                file_content = client_socket.recv(1024)
                if not file_content:
                    break
                file.write(file_content)

        print(f"[RECEIVED] {file_name} from {client_address}")
    except Exception as e:
        print(f"[ERROR] An error occurred while handling the client: {e}")
    finally:
        client_socket.close()

def handle_client_getting_file(client_socket, client_address):
    server.send(list_of_files.encode())
    file_name = client_socket.recv(1024).decode()
    
    chosen_file_directory = os.path.join(file_directory, file_name)
    try:
        with open(chosen_file_directory, 'rb') as f:
             file_data = f.read()
    
        server.sendall(file_data)
    except Exception as e:
        print(f"[ERROR]: Exception {e}")
    finally:
        server.close()

def start_server():
    server.listen()
    print("[RUNNING]")
    client_socket, client_address = server.accept()
    print(f"[HANDLING] {client_address}")
    user_command = client_socket.recv(1024).decode()
    if user_command == "SAVEFILE":
        handle_client_sending_file(client_socket, client_address)
    elif user_command == "GETFILE" and len(list_of_files) > 0:
        handle_client_getting_file(client_socket, client_address)
    else:
        print("[ERROR]: Invalid command")

while True:
    client_socket, client_address = server.accept()
    print(f"[CONNECTED] Connection from {client_address}")

    try:
        user_command = client_socket.recv(1024).decode()
        if user_command == "SAVEFILE":
            handle_client_sending_file(client_socket)
        elif user_command == "GETFILE" and len(list_of_files) > 0:
            handle_client_getting_file(client_socket)
        else:
            print("[ERROR] Invalid command")
    except Exception as e:
        print(f"[ERROR] An error occurred while handling the client: {e}")
    finally:
        client_socket.close()
    
    




