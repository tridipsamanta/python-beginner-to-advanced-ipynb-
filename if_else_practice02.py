sub1 = int(input("Enter marks of English(out of 100) : "))
sub2 = int(input("Enter marks of Math(out of 100) : "))
sub3 = int(input("Enter marks of Science(out of 100) : "))
total = (100*(sub1 + sub2 + sub3))/300
t = sub1+sub2+sub2
print("total marks is :: ",t)
print("Your total percentage is : ",total)

if(total >= 40 and sub1>=33 and sub2>=33 and sub>=33): print("You are passed")
else : print("You are not qualify")

