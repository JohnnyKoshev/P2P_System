# P2P System

This repository contains a Peer-to-Peer (P2P) system implemented in Python. The system allows clients to connect to a server and perform various file-related operations, such as sending files to specific clients, broadcasting files to all connected clients, and receiving files from the other client through the metaserver.

## Server

### server.py

The `server.py` file contains the implementation of the server. It sets up a server socket and listens for incoming client connections. The server handles communication with clients and performs file-related operations based on the client's choice.

#### Dependencies

The server code relies on a utility function `read_property` defined in the `utils.py` file.

#### Configuration

The following server configuration parameters can be modified in the `server.py` file:

- `SERVER_HOST`: The IP address of the server.
- `SERVER_PORT`: The port number of the server.

#### Functionality

The server provides the following functionality:

1. Relay file: The server relays a file from one client to another client. It prompts the requesting client to choose a target client to send the file to.

2. Broadcast file: The server broadcasts a file to all connected clients, except the client that sent the file.

3. Terminate connection: The server terminates the connection with a client.

#### Functions

1. `broadcast_file(client_socket)`: Broadcasts a file to all connected clients except the sender.
    - Args:
        - `client_socket` (socket.socket): The socket of the client sending the file.
    - This function receives the file type and size from the client, followed by the file data. It then iterates through the list of connected clients and sends the file to each client (except the sender).

2. `send_bytes(file_size, file_data, client_socket)`: Sends the file data to the client in chunks.
    - Args:
        - `file_size` (int): Size of the file to be sent.
        - `file_data` (bytes): File data to be sent.
        - `client_socket` (socket.socket): The socket of the client to send the file to.
    - This function sends the file data to the client in chunks until all bytes have been sent.

3. `receive_data(file_size, file_data, client_socket)`: Receives the file data from the client.
    - Args:
        - `file_size` (str): Size of the file to be received.
        - `file_data` (bytes): Initial file data (empty).
        - `client_socket` (socket.socket): The socket of the client sending the file.
    - This function receives the file data from the client in chunks until all bytes have been received.

4. `relay_file(client_socket)`: Relays a file from one client to another client.
    - Args:
        - `client_socket` (socket.socket): The socket of the client requesting the file relay.
    - This function retrieves the IDs of other clients (excluding the requester) and sends the list of available clients to the requester. It then receives the target client ID, file type, file size, and file data from the requester. Finally, it sends the file data to the target client.

5. `handle_client(client_socket, client_address)`: Handles communication with a client.
    - Args:
        - `client_socket` (socket.socket): The socket of the connected client.
        - `client_address` (tuple): The address of the connected client (IP, port).
    - This function continuously receives the client's choice and handles the corresponding actions: relaying a file, broadcasting a file, or terminating the connection.

6. `get_socket_id(socket_tuple)`: Retrieves the socket ID from the socket tuple.
    - Args:
        - `socket_tuple` (tuple): Tuple containing the IP address and port of the socket.
    - This function extracts the socket ID from the socket tuple and returns it as an integer.

7. `start_server()`: Starts the server and listens for client connections.
    - This function creates a server socket, binds it to the specified host and port, and starts listening for client connections. It accepts new client connections and spawns a new thread to handle each client.

#### Running the Server

To start the server, run the `start_server()` function at the end of the `server.py` file.

## Client

### client.py

The `client.py` file contains the implementation of the client. It establishes a connection with the server and allows the user to interact with the server by selecting various options from a menu.

#### Dependencies

The client code relies on the following dependencies:

- `matplotlib`: Used for visualizing image files.
- `pandas`: Used for processing and displaying (in the console) CSV files.
- `json`: Used for processing and displaying (in the console) JSON files.

The required dependencies can be installed using the following command:

```
pip install matplotlib pandas
```

The client code also utilizes a utility function `read_property` defined in the `utils.py` file.

#### Configuration

The following client configuration parameters can be modified in the `client.py` file:

- `SERVER_HOST`: The IP address of the server.
- `SERVER_PORT`: The port number of the server.
- `CLIENT_TIMEOUT`: The timeout duration for sending files (in seconds).

#### Functionality

The client provides the following functionality:

1. Send file: The client sends a file to a specific client selected from a list of available clients provided by the server.

2. Broadcast file: The client broadcasts a file to all connected clients.

3. Receive file: The client receives a file from the server and processes it based on its type (JSON, CSV, or image).

4. Quit: The client terminates the connection with the server.

#### Functions 

1. `menu(socket_id)`: Displays the menu and prompts the user for their choice.
- Args:
    - `socket_id` (str): The ID of the client socket.
Returns:
- `str`: The user's choice.

2. `receive_file(client_socket)`: Receives a file from the server.
- Args:
    - `client_socket` (socket.socket): The client socket.

3. `process_json_file(file_data)`: Processes and displays the contents of a JSON file.
- Args:
    - `file_data` (bytes): The data of the JSON file.

4. `process_csv_file(file_data)`: Processes and displays the contents of a CSV file.
- Args:
    - `file_data` (bytes): The data of the CSV file.

5. `process_image_file(file_data)`: Processes and displays the contents of an image file.
- Args:
    - `file_data` (bytes): The data of the image file.

6. `send_file(client_socket, file_path, choice)`: Sends a file to the server.
- Args:
    - `client_socket` (socket.socket): The client socket.
    - `file_path` (str): The path to the file to be sent.
    - `choice` (str): The user's choice.

7. `start_client()`: Starts the client and establishes a connection with the server.

#### Running the Client

To start the client, run the `start_client()` function at the end of the `client.py` file.

## Utilities

### utils.py

The `utils.py` file contains a utility function `read_property` used by both the server and client code. The function reads a property (string) from a socket until a specified delimiter is encountered.

## Usage

1. Clone the repository:

   ```
   git clone <repository_url>
   ```

2. Start the server:

   ```
   python server.py
   ```

3. Start the client:

   ```
   python client.py
   ```

4. Follow the menu prompts in the client to perform various file-related operations.

Note: Make sure to modify the server configuration parameters (`SERVER_HOST` and `SERVER_PORT`) in both the `server.py` and `client.py` files to match the desired server configuration.

## Demo Screenshots

1. Turning on the server and connecting 4 clients to it


[![Screenshot-2.png](https://i.postimg.cc/NjWNbwmw/Screenshot-2.png)](https://postimg.cc/cvBM42FD)


2. Client menu


[![Screenshot-3.png](https://i.postimg.cc/gJ06Zxjc/Screenshot-3.png)](https://postimg.cc/WDQ3Rb0x)


3. Broadcasting the file (image) from one client to all other clients


[![Screenshot-4.png](https://i.postimg.cc/VNKJmzRx/Screenshot-4.png)](https://postimg.cc/jWJxh0Bc)


4. Saving the image file in order to visualize it then


[![Screenshot-12.png](https://i.postimg.cc/L4tJNdgF/Screenshot-12.png)](https://postimg.cc/kD5MgpyT)


5. Visualizing the received image in other 3 clients


[![Screenshot-5.png](https://i.postimg.cc/3wfX8sCc/Screenshot-5.png)](https://postimg.cc/yJ9gnrGm)


6. Console of the client that received a file 


[![Screenshot-6.png](https://i.postimg.cc/s2bM0sJs/Screenshot-6.png)](https://postimg.cc/Z9FYWkgM)


7. Sending a CSV file from one client to another specified client


[![Screenshot-7.png](https://i.postimg.cc/brwfx22J/Screenshot-7.png)](https://postimg.cc/G8VfrtKw)


8. Receiving a CSV file


[![Screenshot-8.png](https://i.postimg.cc/HkHRXMDC/Screenshot-8.png)](https://postimg.cc/mtXmGtgd)


9. Receiving a JSON file 


[![Screenshot-9.png](https://i.postimg.cc/MGL9PM4H/Screenshot-9.png)](https://postimg.cc/KKn74zmh)


10. Closing a connection on the client-side


[![Screenshot-10.png](https://i.postimg.cc/DycBVYDt/Screenshot-10.png)](https://postimg.cc/tYYhWD95)


11. Server console feedback on the being performed operations


[![Screenshot-11.png](https://i.postimg.cc/C1yjnjXG/Screenshot-11.png)](https://postimg.cc/cKmKV8sC)

## Cisco Packet Tracer Demo

1. System overview. There are 10 devices and one switch that operates as a metaserver among these devices, it supports the whole file-distribution system among end-devices.


[![Screenshot-2.png](https://i.postimg.cc/027fs5WW/Screenshot-2.png)](https://postimg.cc/6y5RVKNn)


2. Test Case. Sending a packet from the Laptop3 to PC3


[![Screenshot-3.png](https://i.postimg.cc/1XQ8cSGX/Screenshot-3.png)](https://postimg.cc/JDp7M9dC)


3. Test Case. Sending a packet from the Laptop3 to PC3. Receiving a packet at the switch


[![Screenshot-4.png](https://i.postimg.cc/kMsJhW9f/Screenshot-4.png)](https://postimg.cc/dD7chkhy)


4. Test Case. Sending a packet from the Laptop3 to PC3. Receiving a packet at PC3


[![Screenshot-5.png](https://i.postimg.cc/pLwRnZYX/Screenshot-5.png)](https://postimg.cc/v4tpJ5Np)


5. IPv4 Configuration pt. 1


[![Screenshot-6.png](https://i.postimg.cc/d1BYpKML/Screenshot-6.png)](https://postimg.cc/gXnQLQ2W)


6. IPv4 Configuration pt. 2. As it is obvious the range of the IPv4 address is between 10.11.38.1 - 10.11.38.10


[![Screenshot-7.png](https://i.postimg.cc/MHNrrsGn/Screenshot-7.png)](https://postimg.cc/tnd5sNWb)


For the packet tracer file itself refer to the `p2p_system.pkt` file located in the root directory.

## Wireshark Analysis

1. Analyzing a file sent in chunks. File type


[![Screenshot-2.png](https://i.postimg.cc/1tbm1Vy4/Screenshot-2.png)](https://postimg.cc/zbSZnBb1)


2. Analyzing a file sent in chunks. File size


[![Screenshot-3.png](https://i.postimg.cc/x8VwPv0G/Screenshot-3.png)](https://postimg.cc/Hc3vY78j)


3. Analyzing a file sent in chunks. File contents


[![Screenshot-4.png](https://i.postimg.cc/TYCsyMWJ/Screenshot-4.png)](https://postimg.cc/ZCvHgQHW)


4. Analyzing a file sent in chunks. Overview of sent chunks


[![Screenshot-5.png](https://i.postimg.cc/hvKCjpDY/Screenshot-5.png)](https://postimg.cc/621VbVGV)


Based on the provided screenshots, we are able to observe the behavior of the P2P system on the background of the console. Here we are able to see how the files are being sent in chunks from one client to another, analyze the being sent files structure, contents and this kind of corresponding features. Wireshark allows us having a clear understanding of the scene running behind the code.

## License

This project is licensed under the MIT License.
