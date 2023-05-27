from typing import Any
from collections import UserList
from datetime import datetime
import re


class Field:

    def __init__(self, value: Any) -> None:
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

    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if re.match('^\\+38\d{10}$', value) or value == '':
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect phone number format! '
                'Please provide correct phone number format.'
            )


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not value:
            Field.value.fset(self, '')
        elif re.match('^\d{2}/\d{2}/\d{4}$', value):
            Field.value.fset(self,
                             datetime.strptime(value, "%d/%m/%Y").date()
                             )
        else:
            raise ValueError(
                'Incorrect date! Please provide correct date format.')


class Record:

    def __init__(self, name: Name, phone: Phone | None = None, birthday: Birthday | None = None):
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

    def __repr__(self) -> str:
        return f'Record (Name:"{self.name}", Phone:"{self.phone}", Birthday:"{self.birthday}")'

    def __str__(self) -> str:
        return f'Name: {self.name}, Phone:{self.phone or "Empty"}, Birthday:{self.birthday or "Empty"}'

    @property
    def record(self):
        return {
            'name': self.name.value,
            'phone': self.phone.value if self.phone else 'Empty',
            'birthday': self.birthday.value if self.birthday else 'Empty'
        }

    def __getitem__(self, item: str):
        return self.record.get(item)


class AddressBook(UserList):

    def __init__(self) -> None:
        self.data: list[Record] = []

    def __getitem__(self, index):
        return self.data[index]

    def create_and_add_record(self, name, phone: str, birthday: str | None = None):
        record = Record(Name(name), Phone(phone), Birthday(birthday))
        self.add_record_handler(record)

        return f"Added contact {record}"

    def add_record_handler(self, record: Record):
        self.data.append(record)

    def change_handler(self, name: str, phone: str):  # зміна телефону
        old_phone = 'Empty'
        for record in self.data:
            if record.name.value == name:
                if record.phone:
                    old_phone = record.phone.value
                record.phone = Phone(phone)

                return (
                    f'For user [ {name} ] had been changed phone number! \n'
                    f' Old phone number: {old_phone} \n'
                    f' New phone number: {record.phone.value}'
                )
        return f'Not found contact for name {name}'

    def phone_handler(self, name: str):  # показати номер телефону
        for record in self.data:
            if record.name.value == name:
                return f"Phone of {name} is: {record['phone']}"
        return f"Phone for user {name} not found"

    def show_all_handler(self):
        result = ''
        header = '='*51 + '\n' + \
            '|{:^5}|{:<12}|{:^15}|{:^14}|\n'.format(
                'No.', 'Name', 'Phone', 'Birthday') + '='*51 + '\n'
        foter = '='*51 + '\n'
        counter = 0
        for record in self.data:
            counter += 1
            result += '|{:^5}|{:<12}|{:^15}|{:^14}|\n'.format(
                counter, record['name'], record['phone'], record['birthday'])
        counter = 0
        result_tbl = header + result + foter
        return result_tbl


if __name__ == "__main__":
    USERS = AddressBook()
    n = Name('Andy')
    b = Phone('07098609')
    record = Record(n, b)

    USERS.add_record_handler(record)

    # USERS[n.value] = b.value

    print(USERS)
    print(USERS.show_all_handler())
