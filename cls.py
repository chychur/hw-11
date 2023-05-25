from collections import UserList
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
        self.record = {
            'name': self.name,
            'phone': self.phone,
            'birthday': self.birthday
        }

    def days_to_birthday(self):
        if not self.birthday:
            return
        now = datetime.now()
        if (self.birthday.value.replace(year=now.year) - now).days > 0:
            return (self.birthday.value.replace(year=now.year) - now).days
        return (self.birthday.value.replace(year=now.year) + 1).days
    
    def __str__(self) -> str:
        return f'Name: {self.name} | Phone: {self.phone} | Birthday : {self.birthday}'


class AddressBook(UserList):

    def __init__(self) -> None:
        self.data = []

    def __getitem__(self, index):
        return self.data[index]
    
    def input_error(func):
        def inner(*args):
            try:
                result = func(*args)
                return result
            except KeyError:
                return "No user"
            except ValueError:
                return 'Give me name and phone please'
            except IndexError:
                return 'Enter user name'
        return inner

    @input_error
    def add_record_handler(self, record=Record):
        self.data.append(record)

    @input_error
    def change_handler(self, name, phone):  # зміна телефону
        name = Name(name)
        phone = Phone(phone)
        for record in self.data:
            old_phone = record['phone']
            if name.value == record['name']:
                record['phone'] = phone.set_value

        return f'For user [ {name.value} ] had been changed phone number! \n Old phone number: {old_phone} \n New phone number: {phone.value}'
    
    @input_error
    def phone_handler(self, name, phone): # показати номер телефону
        name = Name(name)
        phone = Phone(phone)
        for record in self.data:
            if name.value == record['name']:
                record['phone'] = phone
        
        return f'Phone of {name.value} is: {phone}\n'
    
    @input_error
    def show_all_handler(self):
        result = ''
        header = '='*34 + '\n' + \
            '|{:^4}|{:<12}|{:^14}|{:^14}|\n'.format(
            'No.', 'Name', 'Phone', 'Birthday') + '='*48 + '\n'
        foter = '='*48 + '\n'
        counter = 0
        for record in self.data:
            counter += 1
            result += '|{:^4}|{:<12}|{:^14}|{:^14}|\n'.format(
                counter, record['name'], record['value'], record['birthday'])
        counter = 0
        result_tbl = header + result + foter
        return result_tbl


if __name__ == "__main__":
    USERS = AddressBook()
    print(USERS)
    n = Name('Andy')
    b = Phone('07098609')
    record = Record(n, b)

    USERS.add_record_handler(record)

    # USERS[n.value] = b.value
    print(USERS, n, b, record)
    USERS.show_all_handler
