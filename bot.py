from cls import AddressBook, Record, Name, Phone, Birthday

class Bot:
    
    def __init__(self):
        self.adressbook = AddressBook()       

    def parse_input(self, user_input):
        command, *args = user_input.split()
        command = command.lstrip()

        try:
            handler = self.HANDLERS[command.lower()]
        except KeyError:
            if args:
                command = command + ' ' + args[0]
                args = args[1:]
            handler = self.HANDLERS.get(command.lower(), self.unknown_command_handler)

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
        'add': AddressBook.add_record_handler,    # додавання запису
        'change': AddressBook.change_handler,     # зміна телефону
        'show all': AddressBook.show_all_handler, # показати вміст
        'phone': AddressBook.phone_handler,       # показати телефон
        'exit': exit_handler,                     # вихід
        'goodbye': exit_handler,                  # вихід
        'close': exit_handler,                    # вихід
        }

    def run(self):
        while True:
            # example: add Petro 0991234567
        
            user_input = input('Please enter command and args: ')
            handler, name, phone, birthday = self.parse_input(user_input)
            print(handler, name, phone, birthday)
            if name == None:
                result = handler()
            elif birthday == None:
                result = handler(name, phone)
            else:
                result = handler(name, phone, birthday)

            if not result:
                print('Good bye!')
                break
            print(result)


if __name__ == "__main__":
    my_bot = Bot()
    my_bot.run()    
