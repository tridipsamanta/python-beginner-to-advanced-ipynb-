num = input("Enter a  positive number : ")

sum = 0
for i in num:
    sum += int(i)
if int(num)%sum==0:
    print("Harshad number ")
else:
    print("Not harshad nuber...")