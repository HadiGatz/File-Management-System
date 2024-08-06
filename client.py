import socket
import os

HOST = '127.0.0.1'
PORT = 8820

# connecting to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

operation = input("Enter your operation (SAVEFILE/GETFILE): ")

def print_formatted_list(file_list):
    print("List of available files: ")
    print("-----------------------")
    for file in file_list:
        print(file)
    print("-----------------------")

def SAVEFILE():
    # sending the command to the server
    client_socket.send("SAVEFILE".encode())

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
    # sending the command to the server
    client_socket.send("GETFILE".encode())

    # receiving the list of files
    files_list = eval(client_socket.recv(1024).decode())
    print_formatted_list(files_list)

    chosen_file = input("Enter the file of your choice: ")
    if chosen_file in files_list:
        client_socket.send(chosen_file.encode())
        save_directory = input("Enter the directory to save the file: ").strip().replace("\"", "")
        if not os.path.exists(save_directory):
            try:
                os.makedirs(save_directory)
                print(f"Directory created: {save_directory}")
            except Exception as e:
                print(f"Exception {e}")
        save_path = os.path.join(save_directory, chosen_file)
        
        with open(save_path, 'wb') as file:
            while True:
                file_data = client_socket.recv(1024)
                if not file_data:
                    break
                file.write(file_data)
        print(f"File saved to {save_directory}")
    else:
        print("Error: File not found in the list")

if operation == "SAVEFILE":
    SAVEFILE()
elif operation == "GETFILE":
    GETFILE()
else:
    print("Error: Enter a valid operation")

client_socket.close()
