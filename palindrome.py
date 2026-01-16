num = int(input('Enter a positive number : '))
s = 0
temp = num
while num > 0:
    r = num % 10
    s = s*10 + r
    num = num//10
if temp==s:
    print(f'{temp} is a pllindrome number')
else:
    print(f"{temp} is not a Pallindrome number")
