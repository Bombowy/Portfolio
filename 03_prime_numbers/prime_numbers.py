import math
def prime_numbers(start_number,end_number):
    #Prime numbers cannot be less than 2
    if start_number < 2:
        start_number = 2
    list_of_numbers = list(range(start_number,end_number +1))
    #Prime numbers using the Sieve of Eratosthenes method
    for i in range(2,math.isqrt(end_number)):
        for number in list_of_numbers[:]:
            if number % i == 0 and number != i:
                list_of_numbers.remove(number)
    return list_of_numbers
try:
    start_number = int(input('Enter the start number: '))
    end_number = int(input('Enter the end number: '))
except ValueError:
    print("Please enter a valid integer.")

print(prime_numbers(start_number,end_number))