num = int(input('Enter a positive number : '))
s = 0
temp = num
order = len(str(num))
while num > 0:
    r = num % 10
    s = s + r**order
    num = num//10
if temp==s:
    print(f'{temp} is a Amstrong number')
else:
    print(f"{temp} is not a Amstrong number")
