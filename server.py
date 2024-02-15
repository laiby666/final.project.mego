import sys
import os
from customer import Customer
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
        print("Bye...")
        break
