import socket
import os

HOST = '127.0.0.1'
PORT = 8820

# SAVEFILE - sends a file to the server
# GETFILE - gets a lists of files from the server, then gets the file 



# connecting to the server
client_socket = socket.socket()
client_socket.connect((HOST, PORT))

operation = input("Enter your operation: ")



def SAVEFILE():
    # getting the file and its name
    file_directory = input("Enter the address of your file: ").strip().strip('"')
    file_basename = os.path.basename(file_directory)

    # reading the content of the file
    with open(file_directory, 'rb') as f:
       file_data = f.read()

    # sending the length of the file name
    file_name_length = len(file_basename.encode())
    client_socket.send(file_name_length.to_bytes(2, byteorder='big'))

    # sending the file name
    client_socket.send(file_basename.encode(encoding='utf-8'))

    # sending the file data in chunks
    client_socket.sendall(file_data)

    print("Information sent to the server")

def GETFILE():
    pass

if operation == "SAVEFILE":
    SAVEFILE()
elif operation == "GETFILE":
    GETFILE()
else:
    print("Error: Enter a valid operation")

client_socket.close()
