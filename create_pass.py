import string
import random

lower_characters = string.ascii_lowercase
upper_characters = string.ascii_uppercase
numbers = string.digits
signs = string.punctuation


def create_password():
    password = ""

    for i in range(12):
        choice = random.randint(1, 4)

        if choice == 1:
            password += random.choice(lower_characters)
        elif choice == 2:
            password += random.choice(upper_characters)
        elif choice == 3:
            password += random.choice(numbers)
        elif choice == 4:
            password += random.choice(signs)

    return password
