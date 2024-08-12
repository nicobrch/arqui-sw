import socket

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Simulate user input for username and password
username = input("Enter username: ")
password = input("Enter password: ")

# Send credentials to the server
client_socket.send(f"{username},{password}".encode())

# Receive response from the server
response = client_socket.recv(1024).decode()
print(response)

client_socket.close()
