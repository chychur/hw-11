from new import AddressBook, Record, Name, Phone, Birthday

USERS = AddressBook()

# decorator


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


def unknown_command_handler():
    return "unknown_command"


def hello_handler():
    return "How can I help you?"


def exit_handler():
    return


@input_error
def add_handler(name, phone, birthday):
    name = Name(name)
    phone = Phone(phone)
    birthday = Birthday(birthday)
    record = Record(name, phone, birthday)
    USERS.add_record(record)

    return f'User {name.value} added!'


@input_error
def change_handler(name, phone):  # change phone
    name = Name(name)
    phone = Phone(phone)
    old_phone = USERS[name.value]
    

    USERS[name.value] = phone.set_value
    return f'For user [ {name.value} ] had been changed phone number! \n Old phone number: {old_phone} \n New phone number: {phone.value}'


def show_all_handler():
    result = ''
    header = '='*34 + '\n' + \
        '|{:^4}|{:<12}|{:^14}|\n'.format(
            'No.', 'Name', 'Phone') + '='*34 + '\n'
    foter = '='*34 + '\n'
    counter = 0
    for name, phone in USERS.items():
        counter += 1
        result += '|{:^4}|{:<12}|{:^14}|\n'.format(
            counter, name.value, phone.value)
    counter = 0
    result_tbl = header + result + foter
    return result_tbl


@input_error
def phone_handler(name, phone):
    name = Name(name)
    phone = Phone(phone)
    for name, pnone in USERS.items():
        return f'Phone {name.value} is: {pnone.value}\n'


HANDLERS = {
    'hello': hello_handler,
    'add': add_handler,
    'change': change_handler,
    'show all': show_all_handler,
    'phone': phone_handler,
    'exit': exit_handler,
    'goodbye': exit_handler,
    'close': exit_handler,
}


def parse_input(user_input):
    command, *args = user_input.split()
    command = command.lstrip()

    try:
        handler = HANDLERS[command.lower()]
    except KeyError:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
        handler = HANDLERS.get(command.lower(), unknown_command_handler)

    try:
        name = args[0]
    except IndexError:
        name = None

    try:
        phone = args[1]
    except IndexError:
        phone = None

    try:
        birthday = args[2]
    except IndexError:
        birthday = None

    return handler, name, phone, birthday


def main():
    while True:
        # example: add Petro 0991234567
        user_input = input('Please enter command and args: ')
        handler, name, phone, birthday = parse_input(user_input)
        if name == None:
            result = handler()
        else:
            result = handler(name, phone, birthday)

        if not result:
            print('Good bye!')
            break
        print(result)


if __name__ == "__main__":
    main()
