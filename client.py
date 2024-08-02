import socket
import os

HOST = '127.0.0.1'
PORT = 8820

# getting the file and its name
file_directory = input("Enter the address of your file: ").strip().strip('"')
file_basename = os.path.basename(file_directory)

# reading the content of the file
with open(file_directory, 'rb') as f:
    file_data = f.read()

# connecting to the server
client_socket = socket.socket()
client_socket.connect((HOST, PORT))

# sending the file name
client_socket.send(file_basename.encode())

# sending the file data in chunks
client_socket.sendall(file_data)

print("Information sent to the server")

client_socket.close()
