dictionary = {}

def add_to_dictionary(key_value):

    dictionary[key_value[0]] = key_value[1]

    for key, value in dictionary.items():
        print(f"{key}: {value}")

user_input = input('Enter key-value pair separated by a space: ')

if user_input.strip():
    key_value = user_input.split()
    if len(key_value) == 2:
        try:

            add_to_dictionary(key_value)
        except ValueError:
            print("Invalid input. Please enter a valid key-value pair.")
    else:
        print("Please enter exactly two values separated by a space.")
else:
    print("No input was entered.")
