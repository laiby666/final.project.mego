from customer import Customer

class Commands:
    def search(self, command:str):       
        if command.startswith("select first name"):
            return self.first_name               
        if command.startswith("select last name"):
            return self.last_name
        if command.startswith("select id"):
            return self.id
        if command.startswith("select phone"):
            return self.phone
        if command.startswith("select debt="):
            return self.debt
        if command.startswith("select date="):
            return self.date
    
    def select(command, customers:list[Customer]):
        found = [] 
        for customer in customers:
            search = Commands.search(customer, command) 
            if search in command:
                found.append(customer)
                print(customer)
        if not found:
            print("Not found") 
                   
    def set(command, customers):
        pass

li = [Customer(*"Moshe,Cohen,12345678,0501234567,-45,12/02/2024".split(",")),
Customer(*"Avraham,Levi,12345644,0501234555,-45,12/02/2024".split(",")),
Customer(*"Meir,Reich,12345655,0501234444,-45,12/02/2024".split(",")),
Customer(*"Noach,Paloch,12345666,0501234566,-45,12/02/2024".split(",")),
Customer(*"Moshe,Cohen,12345678,0501234567,45,13/02/2024".split(","))]
command = "select first name=Meir"
Commands.select(command, li)