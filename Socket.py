import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine's name
host = socket.gethostname()
port = 12345

# Bind the socket to a public host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print("Server listening on port", port)

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print("Connected to", client_address)

# Send a message to the client
message = "Hello, client!"
client_socket.send(message.encode())

# Close the connection
client_socket.close()
