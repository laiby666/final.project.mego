from customer import Customer
import datetime
import socket

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
            return str(self.date)
        else:
            return "Wrong command"
    
    def found(command:str, customers:list[Customer], client_sock)->str:
        found = []
        if "!=" in command:
            for customer in customers:
                search = Commands.search(customer, command)             
                if search not in command:
                    Commands.sort_list_by_debt(found, customer)
        else:
            for customer in customers:
                search = Commands.search(customer, command)
                if search in command:
                    Commands.sort_list_by_debt(found, customer)
        if not found:
            client_sock.sendall("Not found".encode("utf-8"))
        else:
            to_send = ""
            for customer in found:
                to_send += str(customer)
            client_sock.sendall(to_send.encode("utf-8"))

    def debt_less_or_more_than(command:str, customers:list[Customer], client_sock)->str:
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
            client_sock.sendall("Not found".encode("utf-8"))
        else:
            to_send = ""
            for customer in found:
                to_send += str(customer)
            client_sock.sendall(to_send.encode("utf-8"))
    
    def date_before_or_after_this(command:str, customers:list[Customer], client_sock)->str:
        p_date = command[-10:]
        p_day = int(p_date[:2])
        p_month = int(p_date[3:5])
        p_year = int(p_date[6:])
        point = datetime.date(p_year, p_month, p_day)
        found = []
        for customer in customers:
            spl = customer.date.split("/")
            day = int(spl[0])
            month = int(spl[1])
            year = int(spl[2])
            the_date = datetime.date(year, month, day)
            if "<" in command:
                if the_date < point:
                    Commands.sort_list_by_debt(found, customer)
            elif ">" in command:
                if the_date > point:
                    Commands.sort_list_by_debt(found, customer)
        if not found:
            client_sock.sendall("Not found".encode("utf-8"))
        else:
            to_send = ""
            for customer in found:
                to_send += str(customer)
            client_sock.sendall(to_send.encode("utf-8"))
                
    def sort_list_by_debt(list:list[Customer], customer:Customer)->None:
        if not list:
            list.append(customer)
        elif customer.debt >= list[-1].debt:
            list.append(customer)
        elif customer.debt <= list[0].debt:
            list.insert(0, customer)
        else:
            i, j = 0, len(list)-1
            while i<=j:
                mid = (i+j)//2
                if customer.debt > list[mid].debt and customer.debt< list[mid+1].debt:
                    list.insert(mid+1, customer)
                    break
                if customer.debt == list[mid].debt:
                    list.insert(mid, customer)
                    return
                if list[mid].debt < customer.debt:
                    i = mid+1   
                else:
                    j = mid-1
            
    def select(command:str, customers:list[Customer], client_sock:socket)->str:
        if command.startswith(("select debt<","select debt>")):
            Commands.debt_less_or_more_than(command, customers, client_sock)
        elif command.startswith(("select date<","select date>")):
            Commands.date_before_or_after_this(command, customers, client_sock)
        else:
            Commands.found(command, customers, client_sock)

    def set(command:str, customers:list[Customer], filename:str)->None:
        fields:list[str] = command.split(",")
        for field in fields:
            if "first name" in field:
                first_name = field[field.index("=")+1:]
            elif "last name" in field or "second name" in field:
                last_name = field[field.index("=")+1:]
            elif "id" in field:
                id = field[field.index("=")+1:]
            elif "phone" in field:
                phone = field[field.index("=")+1:]
            elif "debt" in field:
                debt = float(field[field.index("=")+1:])
            elif "date" in field:
                date = field[field.index("=")+1:]            
        customer = Customer(first_name.title(), last_name.title(), id, phone, debt, date)
        with open(filename, "a", encoding="utf-8") as w:
            w.write(str(customer))
        Commands.sort_list_by_debt(customers, customer)

    def valid_command(command:str, customers:list[Customer], client_sock:socket)->bool:
        first_name=""
        last_name=""
        id = ""
        phone=""
        debt=0
        the_date=""
        fields:list[str] = command.split(",")        
        for field in fields:
            if "first name" in field:
                first_name = field[field.index("=")+1:]
            elif "last name" in field or "second name" in field:
                last_name = field[field.index("=")+1:]
            elif "id" in field:
                id = field[field.index("=")+1:]
            elif "phone" in field:
                phone = field[field.index("=")+1:]
            elif "debt" in field:
                debt = float(field[field.index("=")+1:])
            elif "date" in field:
                date1 = field[field.index("=")+1:].split("/") 
                day = int(date1[0])
                month = int(date1[1])
                year = int(date1[2])
                the_date = datetime.date(year, month, day)
        to_send = ""
        if not id.isdigit() or len(id) != 9:
            client_sock.sendall("Invalid ID".encode("utf-8"))
            return False
        if not phone.isdigit() or len(phone) != 10 or not phone.startswith("0"):
            client_sock.sendall("Invalid phone number".encode("utf-8"))
            return False
        if debt == 0:
            client_sock.sendall("Missing debt".encode("utf-8"))
            return False
        if not the_date or not isinstance(the_date, datetime.date):
            client_sock.sendall("Invalid date".encode("utf-8"))
            return False
        if not first_name or not last_name:
            client_sock.sendall("Missing name".encode("utf-8"))
            return False
        for customer in customers:
            if customer.id == id:
                if customer.phone != phone:
                    customer.phone = phone
                    to_send += "Phone number has been updated."
                if customer.first_name != first_name or customer.last_name != last_name:
                    to_send += "The name entered is different from the name entered previously."        
        to_send += "Done."
        client_sock.sendall(to_send.encode("utf-8"))
        return True
