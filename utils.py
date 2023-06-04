def read_property(client_socket, delimiter):
    # transform in bytes array
    property_data = b''
    # read until the delimiter occurs
    while True:
        chunk = client_socket.recv(1)
        if not chunk or chunk == delimiter.encode():
            break
        property_data += chunk
    return property_data
