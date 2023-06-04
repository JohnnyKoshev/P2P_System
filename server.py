"""""

Name: Komiljon Yuldashev
Project: P2P System. Server-side
Description: Provides a needed functionality for the metaserver that serves as a interchange point among the clients

"""""


import socket  # for sockets functionality
import threading  # for processing multiple clients simultaneously
import time  # for timing

from utils import read_property  # for reading a property until a delimiter

# Server configuration
SERVER_HOST = '127.0.0.1'  # Server IP address
SERVER_PORT = 8000  # Server port number

# Client connections
clients = []  # List to store client sockets
clients_socket_ids = []  # List to store socket IDs of clients


def broadcast_file(client_socket):
    """
    Broadcasts a file to all clients except the sender.

    Args:
        client_socket (socket.socket): The socket of the client sending the file.
    """
    # Get the file type and size from the client
    start_file_type = read_property(client_socket, '|').decode().strip()
    start_file_size = read_property(client_socket, '|').decode().strip()

    # Receive the file data from the client
    file_data = receive_data(start_file_size, b'', client_socket)

    # Iterate through the list of clients and send the file to each client (except the sender)
    for client in clients:
        retries = 3
        is_failed = False
        while retries > 0:
            try:
                if client != client_socket:
                    file_size = start_file_size
                    file_type = start_file_type

                    # Send the file type and size to the client with delimiters
                    file_type_msg = f"{file_type}|"
                    file_size_msg = f"{file_size}|"
                    client.sendall(file_type_msg.encode())
                    client.sendall(file_size_msg.encode())

                    # Send the file data in chunks
                    file_size = int(file_size)
                    send_bytes(file_size, file_data, client)

                    print(
                        f"Broadcasted file from the socket {get_socket_id(client_socket.getpeername())} to the socket {get_socket_id(client.getpeername())}.")
            except socket.error as e:
                print(f"Failed to send file to client {get_socket_id(client.getpeername())}: {e}. Retrying")
                retries -= 1
                time.sleep(3)  # Wait for 3 seconds before retrying
                is_failed = True
            finally:
                if not is_failed:
                    retries = 0


def send_bytes(file_size, file_data, client_socket):
    """
    Sends the file data to the client in chunks.

    Args:
        file_size (int): Size of the file to be sent.
        file_data (bytes): File data to be sent.
        client_socket (socket.socket): The socket of the client to send the file to.
    """
    bytes_sent = 0
    while bytes_sent < file_size:
        chunk = file_data[bytes_sent:bytes_sent + 1024]
        client_socket.sendall(chunk)
        bytes_sent += len(chunk)


def receive_data(file_size, file_data, client_socket):
    """
    Receives the file data from the client.

    Args:
        file_size (str): Size of the file to be received.
        file_data (bytes): Initial file data (empty).
        client_socket (socket.socket): The socket of the client sending the file.

    Returns:
        bytes: Complete file data received from the client.
    """
    file_size = int(file_size)
    bytes_received = 0
    while bytes_received < file_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        file_data += chunk
        bytes_received += len(chunk)
    return file_data


def relay_file(client_socket):
    """
    Relays a file from one client to another client.

    Args:
        client_socket (socket.socket): The socket of the client requesting the file relay.
    """
    other_clients_ids = []

    # Get the IDs of other clients (excluding the requester)
    for client_id in clients_socket_ids:
        if get_socket_id(client_socket.getpeername()) != client_id:
            other_clients_ids.append(client_id)

    # Send the list of available clients to the requester
    client_socket.sendall(f'Choose one of the clients to send a file: {str(other_clients_ids)}'.encode())

    # checks if the client selected an appropriate receiving client
    check = client_socket.recv(3).decode().strip()

    if check == "yes":
        # Receive the target client ID from the requester
        target_client = client_socket.recv(20).decode()

        # Receive the file type and size from the requester
        file_type = read_property(client_socket, '|').decode().strip()
        file_size = read_property(client_socket, '|').decode().strip()

        # Receive the file data from the requester
        file_data = receive_data(file_size, b'', client_socket)

        file_size = int(file_size)

        # Send the file data in chunks to the target client
        for client in clients:
            retries = 3
            is_failed = False
            while retries > 0:
                try:
                    if get_socket_id(client.getpeername()) == int(target_client):
                        # adding the delimiter
                        file_type_msg = f"{file_type}|"
                        file_size_msg = f"{file_size}|"
                        # sending the packets
                        client.sendall(file_type_msg.encode())
                        client.sendall(file_size_msg.encode())
                        send_bytes(file_size, file_data, client)

                        print(
                            f"Relayed file from the socket {get_socket_id(client_socket.getpeername())} to the socket {get_socket_id(client.getpeername())}")
                except socket.error as e:
                    print(f"Failed to send file to client: {e}. Retrying")
                    retries -= 1
                    time.sleep(3)  # Wait for 3 seconds before retrying
                    is_failed = True
                finally:
                    if not is_failed:
                        retries = 0
    else:
        return


def handle_client(client_socket, client_address):
    """
    Handles communication with a client.

    Args:
        client_socket (socket.socket): The socket of the connected client.
        client_address (tuple): The address of the connected client (IP, port).
    """
    print(f"New connection from {client_address}")
    while True:
        try:
            # Receive the client's choice
            choice = client_socket.recv(1).decode().strip()

            if choice == '1':  # Relay file
                relay_file(client_socket)
            elif choice == '2':  # Broadcast file
                broadcast_file(client_socket)
            elif choice == '0':  # Terminate connection
                print(f"Closing connection with {client_address}")
                clients.remove(client_socket)
                client_socket.close()
                break

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break


def get_socket_id(socket_tuple):
    """
    Retrieves the socket ID from the socket tuple, which is a return from socket.getpeername().

    Args:
        socket_tuple (tuple): Tuple containing the IP address and port of the socket.

    Returns:
        int: The socket ID.
    """
    socket_id = str(socket_tuple).split(',')[1].strip()
    socket_id = list(socket_id)
    socket_id[-1] = ''
    socket_id = ''.join(socket_id)
    return int(socket_id)


def start_server():
    """
    Starts the server and listens for client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        # saving the clients in the list
        clients.append(client_socket)
        # saving the socket ids of the clients in the list
        clients_socket_ids.append(get_socket_id(client_socket.getpeername()))
        client_socket.sendall(str(get_socket_id(client_socket.getpeername())).encode())
        # making a use of Threads
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        # starting a thread for one client
        client_thread.start()


start_server()
