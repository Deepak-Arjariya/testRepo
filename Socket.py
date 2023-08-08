import socket
import threading

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a host and port
host = socket.gethostname()
port = 12345
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print("Received:", message)
            # Broadcast the message to all clients
            for client in clients:
                client.send(message.encode())
        except:
            break

    clients.remove(client_socket)
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    print("Connected to", client_address)
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
