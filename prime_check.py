n = int(input("Enter a positive number: ")) 
count = 0

if n <= 1:
    print(n, "is not a prime number")
else:
    for j in range(2, n // 2 + 1):
        if n % j == 0:
            count = 1
            break
    if count == 0:
        print(n, "is a prime number")
    else:
        print(n, "is not a prime number")
