from collections import UserDict
from datetime import datetime
import re

class Field:

    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def __str__(self) -> str:
        return f'{self.value}'

    def __repr__(self) -> str:
        return f'{self.value}'



class Name(Field):

    def __init__(self, value) -> None:
        super().__init__(value)



class Phone(Field):

    def __init__(self, value) -> None:
        super().__init__(value)
        self.phone_number = []
    
    @Field.value.setter
    def set_value(self, value):

        while True:
            if value:
                self.phone_number = value
            else:
                try:
                    for number in self.values.split(' '):
                        if re.match('^\+48\d{9}$', number) or re.match('^\\+38\d{10}$', number) or number == '':
                            self.value.append(number)
                        else:
                            raise ValueError
                except ValueError:
                    print('Incorrect phone number format! Please provide correct phone number format.')
                else:
                    break

    def __getitem__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):

        while True:
            if value:
                self.value = value
            else:
                try:
                    if re.match('^\d{2}/\d{2}/\d{4}$', self.value):
                        self.__value = datetime.strptime(self.value.strip(), "%d/%m/%Y").date
                        break
                    elif self.value == '':
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print('Incorrect date! Please provide correct date format.')

    def __getitem__(self):
        return self.value

class Record:

    def __init__(self, name=Name, phone=None | Phone, birthday=None | Birthday):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if not self.birthday:
            return
        now = datetime.now()
        if (self.birthday.value.replace(year=now.year) - now).days > 0:
            return (self.birthday.value.replace(year=now.year) - now).days
        return (self.birthday.value.replace(year=now.year) + 1).days


class AddressBook(UserDict):

    def __init__(self) -> None:
        self.data = {}

    def add_record(self, record=Record):
        self.data[record.name] = record.phone


if __name__ == "__main__":
    USERS = AddressBook()
    print(USERS)
    n = Name('Andy')
    record = Record(n.value, '09013212414')
    USERS.add_record(record)
    b = Phone('07098609')
    USERS[n.value] = b.value
    print(USERS)
