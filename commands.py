from customer import Customer

class Commands:
    def search(self:Customer, command:str):       
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
    
    def found(command:str, customers:list[Customer]):
        found = 0 
        for customer in customers:
            search = Commands.search(customer, command) 
            if search in command:
                found += 1
                print(customer)
        if not found:
            print("Not found") 

    def debt_less_or_more_than(command:str, customers:list[Customer]):
        found = 0
        point = float(command.isdigit())
        for customer in customers:
            if "<" in command:
                if customer.debt > point:
                    print(customer)
                    found += 1
            elif ">" in command:
                if customer.debt < point:
                    print(customer)
                    found += 1
        if not found:
            print("Not found")
    
    def date_before_or_after_this(command:str, customers:list[Customer]):
        pass

    def select(command:str, customers:list[Customer]):
        if command.startswith(("select debt<","select debt>")):
            Commands.debt_less_or_more_than(command, customers)
        elif command.startswith(("select date<","select date>")):
            Commands.date_before_or_after_this(command, customers)
        else:
            Commands.found(command, customers)

    def set(command, customers):
        pass

li = [Customer(*"Moshe,Cohen,12345678,0501234567,-45,12/02/2024".split(",")),
Customer(*"Avraham,Levi,12345644,0501234555,300,12/02/2024".split(",")),
Customer(*"Meir,Reich,12345655,0501234444,-500,12/02/2024".split(",")),
Customer(*"Noach,Paloch,12345666,0501234566,-20,12/02/2024".split(",")),
Customer(*"Moshe,Cohen,12345678,0501234567,45,13/02/2024".split(","))]
command = "select debt<10"
Commands.select(command, li)