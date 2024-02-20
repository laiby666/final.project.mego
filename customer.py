class Customer:
    def __init__(self, first_name, last_name, id, phone, debt, date) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._id = id
        self._phone = phone
        self._debt = float(debt)
        self._date = date

    @property
    def first_name(self):
        return self._first_name
    @property
    def last_name(self):
        return self._last_name
    @property
    def id(self):
        return self._id
    @property
    def phone(self):
        return self._phone    
    @property
    def debt(self):
        return self._debt
    @property
    def date(self):
        return self._date
    
    def add_debt(self, debt):
        if type(debt) is not int:
            print("Error: debt is not an int")
            return
        self._debt += debt

    def __str__(self):
        return f"name: {self._first_name} {self._last_name}, id: {self._id}, phone: {self.phone} debt: {self._debt}"
