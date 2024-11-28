import math
def even_numbers(star_number,end_number):
    list_of_numbers = []
    for i in range(star_number,end_number + 1):
        if i % 2 ==0:
            list_of_numbers.append(i)
    return list_of_numbers
try:
    start_number = int(input('Enter the start number: '))
    end_number = int(input('Enter the end number: '))
except ValueError:
    print("Please enter a valid integer.")

numbers = even_numbers(start_number,end_number)
if len(numbers) == 0:
    print(f'No even numbers in the range from {start_number} to {end_number}.')
else:
    print(f'List of even numbers from the scope {start_number} to {end_number}: ')
rows = range(math.ceil(len(numbers)/10))
#division into lines of 10 numbers
for row in rows:
    if row == rows[-1]:
        print(numbers[row * 10 :])
    else:
        print(numbers[row * 10 : row * 10 + 10])