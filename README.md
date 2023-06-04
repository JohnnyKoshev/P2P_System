# P2P System

This repository contains a Peer-to-Peer (P2P) system implemented in Python. The system allows clients to connect to a server and perform various file-related operations, such as sending files to specific clients, broadcasting files to all connected clients, and receiving files from the server.

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

#### Running the Server

To start the server, run the `start_server()` function at the end of the `server.py` file.

## Client

### client.py

The `client.py` file contains the implementation of the client. It establishes a connection with the server and allows the user to interact with the server by selecting various options from a menu.

#### Dependencies

The client code relies on the following dependencies:

- `matplotlib`: Used for visualizing image files.
- `pandas`: Used for processing and displaying CSV files.

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

## License

This project is licensed under the MIT License.
