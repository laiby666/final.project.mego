import socket

host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
while True:
    command = input("==>").encode('utf-8')
    client_socket.sendall(command)
    data = client_socket.recv(2048)
    print("\r<=" + data.decode('utf-8'), end="\n=>")
