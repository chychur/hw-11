from collections import UserList
from abc import ABC, abstractmethod
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
                    print(
                        'Incorrect phone number format! Please provide correct phone number format.')
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
                        self.__value = datetime.strptime(
                            self.value.strip(), "%d/%m/%Y").date
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

    def __getitem__(self, key):
        result = self.record[key]
        return result

    def __setitem__(self, key, value):
        if key in self.record:
            self.record[key] = value

    def __repr__(self) -> str:
        # return f'Record (Name:"{self.name}", Phone:"{self.phone}", Birthday:"{self.birthday}")'
        return '|{!r:<12}|{!r:^15}|{!r:^14}|\n'.format(self.name, self.phone, self.birthday)

    def __str__(self) -> str:
        return f'Name: {self.name}, Phone:{self.phone or "Empty"}, Birthday:{self.birthday or "Empty"}'


class AddressBook(UserList):

    def __init__(self) -> None:
        self.data = []

    def __getitem__(self, index):
        return self.data[index]

    def create_and_add_record(self, name, phone, birthday):
        record = Record(name, phone, birthday)
        self.add_record_handler(record)

        return f"Added contact {record}"

    def add_record_handler(self, record: Record):
        self.data.append(record)

    def change_handler(self, name, phone, birthday=None):  # зміна телефону
        for rec in self.data:
            new_phone = Phone(phone).value
            if rec['name'] == name:
                old_rec_phone = rec['phone']
                rec['phone'] = new_phone
                print(rec['phone'])

        return f'For user [ {name} ] had been changed phone number! \n Old phone number: {old_rec_phone} \n New phone number: {new_phone.value}'

    def phone_handler(self, name, phone=None, birthday=None):  # показати номер телефону

        for rec in self.data:
            if rec['name'] == name:
                rec_name = rec['name']
                rec_phone = rec['phone']
                return f'Phone of {rec_name} is: {rec_phone}\n'
            else:
                return f'There is no this contact: {rec_name}'

    def show_all_handler(self):
        result = ''
        header = '='*51 + '\n' + '|{:^5}|{:^12}|{:^15}|{:^14}|\n'.format(
                 'No.', 'Name', 'Phone', 'Birthday') + '='*51 + '\n'
        foter = '='*51 + '\n'
        counter = 0
        for record in self.data:
            counter += 1
            result += '|{:^5}'.format(counter)+repr(record)
        counter = 0
        result_tbl = header + result + foter
        return result_tbl

    def __str__(self):
        result = []
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            else:
                birth = ''
            if account['phones']:
                new_value = []
                for phone in account['phones']:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append(
                "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50 + '\n')
        return '\n'.join(result)


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
