import random
'''
1 for Rock
0 for papper
-1 for Scissors
'''
computer = random.choice([-1,0,1])
yourchoice = input("Enter your Choice : ")
yourdict = {"r":1,"p":0,"s":-1}
reversdict = {1:"Rock",-1:"Scissors",0:"papper"}

you = yourdict[yourchoice]

print(f"You Choose : {reversdict[you]}\nComputer Chose : {reversdict[computer]}")

if computer == you:
    print("It's a Draw!")
elif (you == 1 and computer == -1) or (you == -1 and computer == 0) or (you == 0 and computer == 1):
    print("You Win!")
else:
    print("You Lose!")
