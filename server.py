import sys
import os
from customer import Customer, CustomerActions
import threading
import socket

host = '127.0.0.1'
port = 12345 

if len(sys.argv) < 2:
    print("Error: missing csv file name!")
    quit()

csv_file = sys.argv[1]    
if not os.path.exists(csv_file):
    with open(csv_file, "w"):
        pass


customers = []
with open(csv_file, "r") as fd:
    for line in fd.readlines():
        fileds = line.split(",")
        id = fileds[2]
        for customer in customers:
            if customer.id == id:
                customer.add_debt(int(fileds[4]))                
                break
        else:
            customer = Customer(*fileds)
            customers.append(customer)

customers.sort(key=lambda customer: customer.debt)
for customer in customers:
    print(customer)

while True:
    query = input("==> ")
    if query == "quit":
        print("Bye")
        break

def choose_action(client_sock):
    while True:
        command = client_sock.recv(2048).split(" ")
        if command[0] == "select":
            customer.select(command)
        if command[0] == "set":
            customer.set(command)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(40)
while True:
    client_socket, client_address = server_socket.accept()
    t = threading.Thread(target=choose_action, args=(client_socket,))
    t.start()