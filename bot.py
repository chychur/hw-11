from cls import AddressBook, Record, Name, Phone, Birthday


class Bot:

    def __init__(self):
        self.adressbook = AddressBook()

    def parse_input(self, user_input):
        command, *args = user_input.split()
        command = command.lstrip()

        if command.lower() in self.HANDLERS.keys():
            handler = self.HANDLERS[command.lower()]
        elif command.lower() in self.adressbook.COMMAND_ADDRESSBOOK.keys():
            try:
                handler = self.adressbook.COMMAND_ADDRESSBOOK[command.lower()]
            except KeyError:
                if args:
                    command = command + ' ' + args[0]
                    args = args[1:]
                handler = self.adressbook.COMMAND_ADDRESSBOOK.get(
                    command.lower(), self.unknown_command_handler)

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

    def unknown_command_handler():
        return "unknown_command"

    def hello_handler():
        return "How can I help you?"

    def exit_handler():
        return

    HANDLERS = {
        'hello': hello_handler,                   # привітання
        # 'add': AddressBook.add_record_handler,    # додавання запису
        # 'change': AddressBook.change_handler,     # зміна телефону
        # 'show all': AddressBook.show_all_handler,  # показати вміст
        # 'phone': AddressBook.phone_handler,       # показати телефон
        'exit': exit_handler,                     # вихід
        'goodbye': exit_handler,                  # вихід
        'close': exit_handler                     # вихід
    }

    def run(self):
        while True:
            # example: add Petro 0991234567

            user_input = input('Please enter command and args: ')
            handler, name, phone, birthday = self.parse_input(user_input)
            print(handler, self.adressbook, name, phone, birthday)
            if handler in self.HANDLERS.keys():
                result = handler()
                print(result)
            elif handler in self.adressbook.COMMAND_ADDRESSBOOK.keys():

                print(self.adressbook)
                if name == None:
                    result = handler(self.adressbook)
                elif handler == self.adressbook.COMMAND_ADDRESSBOOK['add']:
                    record = Record(name, phone, birthday=None)
                    result = handler(self.adressbook, record)
                    print(result)
                else:
                    result = handler(self.adressbook, name, phone)
                print(result)
            # if not result:
            #     print('Good bye!')
            #     break
            # record = Record(name, phone, birthday=None)
            # result = handler(self.adressbook, record)

            print(self.adressbook)


if __name__ == "__main__":
    my_bot = Bot()
    my_bot.run()
