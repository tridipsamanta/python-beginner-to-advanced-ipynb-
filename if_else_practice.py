a = int(input("Enter first number : "))
b = int(input("Enter second number : "))
c = int(input("Enter third number : "))
d = int(input("Enter Fourth number : "))

if(a > b and a>c and a>d) : print(a,"is Big")
elif(b > a and b>c and b>d) : print(b,"is big")
elif(c>a and c > b and c>d):print(c,"is big")
else : print(d,"is big")