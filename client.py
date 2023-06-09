"""""

Name: Komiljon Yuldashev
Project: P2P System. Client-side
Description: Provides a needed functionality for the client that can perform multiple operations like: 
1) Sending a file to the particular client, 
2) Broadcasting a file to all other clients
3) Receiving a file (staying in the waiting state)
4) Quitting the system (closing the connection with the server)

"""""

import io  # for processing csv files
import json  # for processing json
import os  # for getting a file's meta information
import socket  # for sockets functionality
import time  # for timing

import matplotlib.pyplot as plt  # for processing image files
import pandas as pd  # for processing csv files

from utils import read_property  # for reading a property until a delimiter

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Client configuration
CLIENT_TIMEOUT = 15.0  # Timeout for sending files (in seconds)


def menu(socket_id):
    """
    Displays the menu and prompts the user for their choice.

    Args:
        socket_id (str): The ID of the client socket.

    Returns:
        str: The user's choice.
    """
    print(f"Your socket id: {socket_id}")
    print("Menu:")
    print("1. Send file")
    print("2. Broadcast file")
    print("3. Receive file")
    print("0. Quit")
    choice = input("Enter your choice: ")
    return choice


def receive_file(client_socket):
    """
    Receives a file from the server.

    Args:
        client_socket (socket.socket): The client socket.

    """
    # Receive file type
    file_type = read_property(client_socket, '|').decode().strip()
    # Receive file size
    file_size = int(read_property(client_socket, '|').decode().strip())
    # Receive file data
    file_data = b''
    # send file in chunks
    bytes_received = 0
    while bytes_received < file_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        file_data += chunk
        bytes_received += len(chunk)
    # Process the received file based on its type
    if file_type == 'json':
        process_json_file(file_data)
    elif file_type == 'csv':
        process_csv_file(file_data)
    elif file_type in ['png', 'jpg', 'jpeg']:
        process_image_file(file_data)
    else:
        print(f"Unsupported file type: {file_type}")


def process_json_file(file_data):
    """
    Processes and displays the contents of a JSON file.

    Args:
        file_data (bytes): The data of the JSON file.
    """
    # Convert file data to JSON
    file_content = file_data.decode()
    data = json.loads(file_content)

    # Visualize JSON data
    print("Received JSON data:")
    print(data)


def process_csv_file(file_data):
    """
    Processes and displays the contents of a CSV file.

    Args:
        file_data (bytes): The data of the CSV file.
    """
    # Convert file data to a DataFrame
    file_content = file_data.decode()
    df = pd.read_csv(io.StringIO(file_content), dtype='string')
    # Visualize DataFrame
    print("Received CSV data:")
    print(df)


def process_image_file(file_data):
    """
    Processes and displays the contents of an image file.

    Args:
        file_data (bytes): The data of the image file.
    """
    # Save the image file
    with open('client_received_image.png', 'wb') as file:
        file.write(file_data)

    # Visualize the image using Matplotlib
    img = plt.imread('client_received_image.png')
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def send_file(client_socket, file_path, choice):
    """
    Sends a file to the server.

    Args:
        client_socket (socket.socket): The client socket.
        file_path (str): The path to the file to be sent.
        choice (str): The user's choice.
    """
    try:
        # set the timeout
        client_socket.settimeout(CLIENT_TIMEOUT)
        # obtain file type and insert a delimiter for further sending
        file_name = os.path.basename(file_path)
        file_type = file_name.split('.')[-1]
        file_type_msg = f"{file_type}|"
        # Send file type with delimiter
        client_socket.sendall(file_type_msg.encode())

        # Send file size to server with delimiter
        file_size = os.path.getsize(file_path)
        file_size_msg = f"{file_size}|"
        client_socket.sendall(file_size_msg.encode())

        # Send file data
        with open(file_path, 'rb') as file:
            start_time = time.time()
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                client_socket.sendall(chunk)
            end_time = time.time()

        print(f"File uploaded in {end_time - start_time:.10f} seconds")
    except socket.timeout:
        print("The process of sending has timed out")


def start_client():
    """
    Starts the client and establishes a connection with the server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")
    socket_id = client_socket.recv(10).decode()
    while True:
        choice = menu(socket_id)
        if choice == '1':  # Send file
            client_socket.sendall(choice.encode())
            other_clients_msg = read_property(client_socket, ']').decode() + ']'
            print(other_clients_msg)

            # obtain client socket ids in the form of an array
            other_clients_str = other_clients_msg.split(":")[1].strip()
            other_clients = list(other_clients_str)
            other_clients[0] = ""
            other_clients[-1] = ""
            other_clients = "".join(other_clients)
            other_clients = other_clients.split(",")

            # obtain an input from the user for the target client
            target_client = input()
            check = False
            for client in other_clients:
                # works only for the target client
                if target_client == client.strip():
                    check = True
                    # reliability mechanism
                    client_socket.sendall("yes".encode())
                    client_socket.sendall(target_client.encode())
                    file_path = input("Enter the path of the file to send: ")
                    if os.path.exists(file_path):
                        send_file(client_socket, file_path, choice)
                    else:
                        print("File not found!")
            # reliability mechanism
            if not check:
                client_socket.sendall("no".encode())
                print("Client not found!")

        elif choice == '2':  # Broadcast file
            file_path = input("Enter the path of the file to broadcast: ")
            if os.path.exists(file_path):
                client_socket.sendall(choice.encode())
                send_file(client_socket, file_path, choice)
            else:
                # reliability mechanism
                print("File not found!")

        elif choice == '3':  # Receive file
            receive_file(client_socket)

        elif choice == '0':  # Quit
            print("Closing connection...")
            client_socket.sendall(choice.encode())
            client_socket.close()
            break


start_client()
