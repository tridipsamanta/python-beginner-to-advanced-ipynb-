num = int(input("Enter a number : "))
if num > 1:
    if (num % 4 == 0 and num % 100 != 0) or (num % 400 == 0):
        print(num, "is a leap year.")
    else:
        print(num, "is not a leap year.")