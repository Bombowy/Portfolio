def reverse_string(s):
    return s[::-1]

s = input('Enter string to reverse: ')

if s:
    print(f'Reversed string: {reverse_string(s)}')
else:
    print('No string entered.')

