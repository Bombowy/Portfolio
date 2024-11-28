def add_numbers(*args):
    # Check if all arguments are numbers
    if all(isinstance(arg, (int, float)) for arg in args):
        print(f'The sum is: {sum(args)}')
    else:
        print("All arguments must be numbers.")

# Retrieving data from the user
user_input = input('Enter numbers separated by spaces: ')

# Check if user entered anything
if user_input.strip():
    # transform data into a list
    try:
        numbers = [float(num) for num in user_input.split()]
        # Calling the function
        add_numbers(*numbers)
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
else:
    print("No numbers were entered.")