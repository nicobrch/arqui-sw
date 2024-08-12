import socket
import db

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Server is listening on port 12345...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established!")

    # Receive username and password from the client
    credentials = client_socket.recv(1024).decode()
    username, password = credentials.split(',')
    print(f"Received username: {username}")

    # Check if the username and password are valid
    if db.verify_password(username, password):
        client_socket.send("Login successful!".encode())
        print(f"Login successful for {username}")
    else:
        client_socket.send("Login failed!".encode())
        print(f"Login failed {username}")

    client_socket.close()
