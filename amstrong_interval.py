num1 = int(input('Enter first number  : '))
num2 = int(input('Enter second number : '))
print('Amstrong number are : ')
for i in range(num1,num2+1):
    digit = 0
    q = i
    p = i
    s = 0
    while p != 0:
        digit = digit + 1
        p = p//10
    while q != 0:
        r = q%10
        s = s + (r**digit)
        q = q//10
    if s==i:
        print("",i)
