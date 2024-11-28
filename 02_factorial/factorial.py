def factorial(n):
    if n < 0:
        return "Factorial is not defined for negative numbers."
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# Input walidation
while True:
    try:
        number = int(input("Enter the number to calculate the factorial: "))
        break
    except ValueError:
        print("Please enter a valid integer.")

print(f'Factorial of {number} is {factorial(number)}')
