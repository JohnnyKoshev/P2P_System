import socket
import threading
import sys, os
from utils import read_property

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Client connections
clients = []
clients_socket_ids = []


def broadcast_file(client_socket):
    # Broadcast file to all clients except the sender
    start_file_type = read_property(client_socket, '|').decode().strip()
    start_file_size = read_property(client_socket, '|').decode().strip()
    file_data = receive_data(start_file_type, start_file_size, b'', client_socket)
    for client in clients:
        retries = 3
        is_failed = False
        while retries > 0:
            try:
                if client != client_socket:
                    file_size = start_file_size
                    file_type = start_file_type
                    # Receive file data
                    file_type_msg = f"{file_type}|"
                    file_size_msg = f"{file_size}|"
                    client.sendall(file_type_msg.encode())
                    client.sendall(file_size_msg.encode())
                    # Send file data in chunks
                    file_size = int(file_size)
                    bytes_sent = 0
                    while bytes_sent < file_size:
                        chunk = file_data[bytes_sent:bytes_sent + 1024]
                        client.sendall(chunk)
                        bytes_sent += len(chunk)
                    print(f"Broadcasted file from the socket {get_socket_id(client_socket.getpeername())} to the socket {get_socket_id(client.getpeername())}")
            except socket.error as e:
                print(f"Failed to send file to client {get_socket_id(client.getpeername())}: {e}. Retrying")
                retries -= 1
                time.sleep(3)  # Wait for 3 seconds before retrying
                is_failed = True
            finally:
                if is_failed == False:
                    retries = 0


def receive_data(file_type, file_size, file_data, client_socket):
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
    other_clients_ids = []
    for client_id in clients_socket_ids:
        if get_socket_id(client_socket.getpeername()) != client_id:
            other_clients_ids.append(client_id)
    client_socket.sendall(f'Choose one of the clients to send a file: {str(other_clients_ids)}'.encode())
    check = client_socket.recv(3).decode().strip()
    if check == "yes":
        target_client = client_socket.recv(20).decode()

        # Receive file type
        file_type = read_property(client_socket, '|').decode().strip()
        file_size = read_property(client_socket, '|').decode().strip()
        file_data = receive_data(file_type, file_size, b'', client_socket)

        file_size = int(file_size)
        # Send file data in chunks
        for client in clients:
            retries = 3
            is_failed = False
            while retries > 0:
                try:
                    if get_socket_id(client.getpeername()) == int(target_client):
                        file_type_msg = f"{file_type}|"
                        file_size_msg = f"{file_size}|"
                        client.sendall(file_type_msg.encode())
                        client.sendall(file_size_msg.encode())
                        bytes_sent = 0
                        while bytes_sent < file_size:
                            chunk = file_data[bytes_sent:bytes_sent + 1024]
                            client.sendall(chunk)
                            bytes_sent += len(chunk)
                        print(f"Relayed file from the socket {get_socket_id(client_socket.getpeername())} to the socket {get_socket_id(client.getpeername())}")
                except socket.error as e:
                    print(f"Failed to send file to client: {e}. Retrying")
                    retries -= 1
                    time.sleep(3)  # Wait for 3 seconds before retrying
                    is_failed = True
                finally:
                    if is_failed == False:
                        retries = 0
    else:
        return

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    while True:
        try:
            # Receive client's choice
            choice = client_socket.recv(1).decode().strip()
            if choice == '1':  # Relay file
                relay_file(client_socket)
            elif choice == '2':  # Broadcast file
                # Broadcast file to all clients except the sender
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
    socket_id = str(socket_tuple).split(',')[1].strip()
    socket_id = list(socket_id)
    socket_id[-1] = ''
    socket_id = ''.join(socket_id)
    return int(socket_id)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        clients_socket_ids.append(get_socket_id(client_socket.getpeername()))
        client_socket.sendall(str(get_socket_id(client_socket.getpeername())).encode())
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


start_server()
