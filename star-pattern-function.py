n = int(input("Enter a positive number : "))

def star(n):
    if(n==0):
        return
    print("*"*n)
    star(n-1)
print(star(n))
