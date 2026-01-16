def big(a,b,c):
    if(a>b and a>c):
        print(a,"is Big")
    elif(b>c and b>a):
        print(b,"is Big")
    else:
        print(c,"is Big")

x = int(input("Enter first number : "))
y = int(input("Enter second number : "))
z = int(input("Enter third number : "))

big(x,y,z)

def big1(a,b,c):
    if(a>b and a>c):
        return a
    elif(b>c and b>a):
       return b
    else:
        return c


print("Big number is ",big1(x,y,z))

