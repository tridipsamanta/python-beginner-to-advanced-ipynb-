# palindrome number check........
num = input("Enter a positive number : ")

if num == num[::-1]:
    print("Pallindrome..")
else:
    print("Not pallindrome...")