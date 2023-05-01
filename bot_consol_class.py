from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = phones or []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return True
        return False


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, search_str):
        results = []
        for record in self.data.values():
            if search_str.lower() in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if search_str in phone.value:
                        results.append(record)
                        break
        return results


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, ValueError, IndexError) as f:
            return str(f)
    return inner


@input_error
def handle_hello():
    return "How can I help you?"


@input_error
def handle_add(name, phone, address_book):
    if len(name.strip()) == 0 or len(phone.strip()) == 0:
        raise ValueError("Please enter both name and phone number")
    record = address_book.get(name.lower())
    if not record:
        record = Record(name)
        address_book.add_record(record)
    record.add_phone(phone)
    return f"Added phone {phone} for contact {name}"


@input_error
def handle_change(name, old_phone, new_phone, address_book):
    record = address_book.get(name.lower())
    if not record:
        raise KeyError(f"{name} is not in contacts")
    if not record.edit_phone(old_phone, new_phone):
        raise ValueError(f"{old_phone} is not in {name}'s phones")
    return f"Changed phone {old_phone} to {new_phone} for contact {name}"


@input_error
def handle_phone(name, address_book):
    record = address_book.get(name.lower())
    if not record:
        raise KeyError(f"{name} is not in contacts")
    return "\n".join([phone.value for phone in record.phones])


@input_error
def handle_show_all(address_book):
    return "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in address_book.items()])


@input_error
def handle_search(search_str, address_book):
    if len(search_str.strip()) == 0:
        raise ValueError("Please enter a search string")
    split_command = search_str.split()
    if len(split_command) < 2:
        raise ValueError(
            "Invalid search format. Please enter a search string and try again.")
    results = address_book.search(split_command[1])
    if not results:
        return f"No contacts found for '{split_command[1]}'"
    else:
        return "\n".join([f"{record.name.value}: {', '.join([phone.value for phone in record.phones])}" for record in results])


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").lower()
        if command == "hello":
            print(handle_hello())
        elif command == '.':
            break
        elif command.startswith("add"):
            try:
                name, phone = command.split()[1:]
                print(handle_add(name, phone, address_book))
            except ValueError as e:
                print(str(e))
        elif command.startswith("change"):
            try:
                name, old_phone, new_phone = command.split()[1:]
                print(handle_change(name, old_phone, new_phone, address_book))
            except ValueError as e:
                print(str(e))
            except KeyError as e:
                print(str(e))
        elif command.startswith("phone"):
            try:
                name = command.split()[1]
                print(handle_phone(name, address_book))
            except KeyError as e:
                print(str(e))
        elif command == "show all":
            print(handle_show_all(address_book))
        elif command.startswith("search"):
            try:
                search_str = command.split()[1]
                print(handle_search(search_str, address_book))
            except IndexError:
                print("You have entered insufficient arguments")
            except ValueError as e:
                print(str(e))
        elif command in ("good bye", "close", "exit",):
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == '__main__':
    main()
