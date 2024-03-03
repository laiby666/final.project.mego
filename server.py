import sys
import os
from customer import Customer
import threading
import socket
from commands import Commands
host = '127.0.0.1'
port = 12345 

if len(sys.argv) < 2:
    print("Error: missing csv file name!")
    quit()

csv_file = sys.argv[1]    
if not os.path.exists(csv_file):
    with open(csv_file, "w"):
        pass

customers:list[Customer] = []
with open(csv_file, "r") as fd:
    for line in fd.readlines():
        fields = line.split(",")
        id = fields[2]
        for customer in customers:
            if customer.id == id:
                customer.add_debt(float(fields[4]))                
                break
        else:
            customer = Customer(*fields)
            Commands.sort_list_by_debt(customers, customer)

mutex = threading.Lock()
def choose_action(client_sock):
    while True:
        command:str = client_sock.recv(2048).decode("utf-8")
        command.lower()
        if command == "print":
            Commands.print_data(customers)
        elif "select" in command:
            Commands.select(command, customers, client_sock)            
        elif "set" in command:
            if Commands.valid_command(command, customers, client_sock):
                with mutex:
                    Commands.set(command, customers, csv_file)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(40)
while True:
    client_socket, client_address = server_socket.accept()
    t = threading.Thread(target=choose_action, args=(client_socket,))
    t.start()
