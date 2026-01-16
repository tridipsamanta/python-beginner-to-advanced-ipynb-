a = int(input("Enter first variable : "))
b = int(input("Enter Second variable : "))

def big(a,b):
    if(a==b):
        return a
    else:
        if(a>b):
            return a
        else:
            return b
        
print("Big is : ",big(a,b))