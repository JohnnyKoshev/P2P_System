def read_property(client_socket, delimiter):
    property_data = b''
    while True:
        chunk = client_socket.recv(1)
        if not chunk or chunk == delimiter.encode():
            break
        property_data += chunk
    return property_data
