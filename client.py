import socket
import os

HOST = '127.0.0.1'
PORT = 8820

# getting the file and its name
file_directory = input("Enter the address of your file: ")
file_basename = os.path.basename(file_directory)

# reading the content of the file
with open(file_directory, 'r') as f:
    file_data = f.read()

# connecting to the server
client_socket = socket.socket()
client_socket.connect((HOST, PORT))

# sending the file name
client_socket.send(file_basename.encode())

# sending the file data
client_socket.send(file_data.encode())

print("Information sent to the server")

client_socket.close()
