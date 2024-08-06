from functools import wraps
from typing import List
from address_book import AddressBook
from record import Record

def input_error(func):
    """
    Decorator to handle input errors and return error messages.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return inner


@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    """
    Adds a contact to the address book.

    Args:
        args (List[str]): The arguments for the command.
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    if len(args) < 2:
        raise ValueError("Error: Give me name and phone please.")
    
    name, phone, *optional_args = args
    birthday = optional_args[0] if optional_args else None
    
    existing_record = book.find(name)
    if existing_record and any(phone == p.value for p in existing_record.phones):
        return "Contact with this name and phone number already exists."
    
    if existing_record:
        existing_record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        if birthday:
            record.add_birthday(birthday)
        book.add_record(record)
        return "Contact added."

    return "Contact updated."

@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    """
    Changes a phone number for an existing contact or removes a phone number if only two arguments are provided.

    Args:
        args (List[str]): The arguments for the command.
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    if len(args) == 3:
        # Three arguments: change the phone number
        name, old_phone, new_phone = args
        record = book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return "Phone number updated."
        return "Contact not found."
    
    elif len(args) == 2:
        # Two arguments: remove the phone number
        name, phone_to_remove = args
        record = book.find(name)
        if record:
            if record.find_phone(phone_to_remove):
                record.remove_phone(phone_to_remove)
                return "Phone number removed."
            else:
                return "Phone number not found in the contact."
        return "Contact not found."
    
    else:
        raise ValueError("Error: Give me name, old phone and new phone please or name and phone to remove.")

@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    """
    Shows the phone number for the specified contact.

    Args:
        args (List[str]): The arguments for the command.
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    if len(args) != 1:
        raise ValueError("Error: Give me name, please.")
    
    name = args[0]
    record = book.find(name)
    if record:
        phones = ", ".join([str(phone) for phone in record.phones])
        return f"{name}: {phones}"
    return "Contact not found."

@input_error
def show_all(book: AddressBook) -> str:
    """
    Shows all contacts in the address book.

    Args:
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    if not book:
        return "The address book is empty."
    
    return "\n".join([str(record) for record in book.values()])

@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    """
    Adds a birthday to the specified contact.

    Args:
        args (List[str]): The arguments for the command.
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    if len(args) != 2:
        raise ValueError("Error: Give me name and birthday please.")
    
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    """
    Shows the birthday for the specified contact.

    Args:
        args (List[str]): The arguments for the command.
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    if len(args) != 1:
        raise ValueError("Error: Give me name, please.")
    
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {record.birthday}"
    return "Contact not found."

@input_error
def birthdays(args: List[str], book: AddressBook) -> str:
    """
    Shows upcoming birthdays within the next 7 days.

    Args:
        args (List[str]): The arguments for the command.
        book (AddressBook): The address book instance.

    Returns:
        str: The response message.
    """
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No birthdays in the next 7 days."
    return "\n".join(
        f"Upcoming birthday within the next week: {record.name} - {record.birthday}, Phones: {', '.join(str(phone) for phone in record.phones)}"
        for record in upcoming_birthdays
    )