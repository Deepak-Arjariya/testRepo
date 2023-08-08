Certainly! Here's a simple example of a client-server communication using sockets in Python. You can run this code in Windows Subsystem for Linux (WSL) to test the basic socket communication between a client and a server.

1. **Server (Python):**
Save this code in a file named `server.py`:

```python
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
```

2. **Client (Python):**
Save this code in a file named `client.py`:

```python
import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine's name
host = socket.gethostname()
port = 12345

# Connect to the server
client_socket.connect((host, port))

# Receive data from the server
data = client_socket.recv(1024).decode()
print("Received:", data)

# Close the connection
client_socket.close()
```

Now, open two terminal windows in your WSL:

1. In the first terminal, navigate to the folder containing `server.py` and run the server:
   ```
   python3 server.py
   ```

2. In the second terminal, navigate to the folder containing `client.py` and run the client:
   ```
   python3 client.py
   ```

You should see the server and client exchanging a message. The server waits for a client to connect, and once the client connects, it sends a "Hello, client!" message back to the client.

This example demonstrates a basic socket communication between a client and a server running on the same machine. You can further explore and modify the code to experiment with different scenarios and functionalities.
