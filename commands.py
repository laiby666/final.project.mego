from customer import Customer
import datetime
import re

class Commands:
    def search(self:Customer, command:str)->str:       
        if command.startswith("select first name"):
            return self.first_name               
        if command.startswith("select last name"):
            return self.last_name
        if command.startswith("select id"):
            return self.id
        if command.startswith("select phone"):
            return self.phone
        if command.startswith(("select debt=","select debt!=")):
            num = str(command.isdigit())
            if "." not in num:
                debt = int(self.debt)
                return str(debt)
            else:
                return str(self.debt)
        if command.startswith(("select date=","select date!=")):
            return self.date
    
    def found(command:str, customers:list[Customer]):
        found = []
        for customer in customers:
            search = Commands.search(customer, command) 
            if "!=" in command:
                if search not in command:
                    Commands.sort_list_by_debt(found, customer)
            else:
                if search in command:
                    Commands.sort_list_by_debt(found, customer)
        if not found:
            print("Not found") 
        else:
            [print(customer) for customer in found]

    def debt_less_or_more_than(command:str, customers:list[Customer]):
        found = []
        point = float(command.isdigit())
        for customer in customers:
            if "<" in command:
                if customer.debt > point:
                    Commands.sort_list_by_debt(found, customer)
            elif ">" in command:
                if customer.debt < point:
                    Commands.sort_list_by_debt(found, customer)
        if not found:
            print("Not found")
        else:
            [print(customer) for customer in found]
    
    def date_before_or_after_this(command:str, customers:list[Customer]):
        p_date = command[-10:]
        p_day = int(p_date[:2])
        p_month = int(p_date[3:5])
        p_year = int(p_date[6:])
        point = datetime.date(p_year, p_month, p_day)
        found = []
        for customer in customers:
            day = int(customer.date[:2])
            month = int(customer.date[3:5])
            year = int(customer.date[6:])
            the_date = datetime.date(year, month, day)
            if "<" in command:
                if the_date < point:
                    Commands.sort_list_by_debt(found, customer)
            elif ">" in command:
                if the_date > point:
                    Commands.sort_list_by_debt(found, customer)
        if not found:
            print("Not found")
        else:
            [print(customer) for customer in found]
                
    def sort_list_by_debt(list:list[Customer], customer:Customer)->None:
        if not list:
            list.append(customer)
        elif customer.debt >= list[-1].debt:
            list.append(customer)
        elif customer.debt <= list[0].debt:
            list.insert(0, customer)
        else:
            for i in range(len(list)):
                if customer.debt <= list[i].debt:
                    list.insert(i, customer)
                    break

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
Customer(*"Avraham,Levi,12345644,0501234555,300,11/01/2024".split(",")),
Customer(*"Meir,Reich,12345655,0501234444,-500,12/01/2024".split(",")),
Customer(*"Noach,Paloch,12345666,0501234566,-20,12/02/2024".split(",")),
Customer(*"Moshe,Cohen,12345678,0501234567,-55,13/02/2024".split(","))]
command = "select first name!=Moshe"
Commands.select(command, li)