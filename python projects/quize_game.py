print("Welcome to my computer Quize game :) ")

playing = input("Do you want to play? ").lower()

if playing != 'yes':
    quit()
print("Okay Let's play :) \n")
score = 0
answer = input("What does CPU stand for ? ").lower()
if answer == 'central processing unit':
    print("Correct answer !! ")
    score += 1
else:
    print("OOpps Wrong answer !! ")

answer = input("What does RAM stand for? ").lower()
if answer == "random access memory":
    print("Correct answer!!")
    score += 1
else:
    print("Oops! Wrong answer!!")

answer = input("What does HTML stand for? ").lower()
if answer == "hypertext markup language":
    print("Correct answer!!")
    score += 1
else:
    print("Oops! Wrong answer!!")

answer = input("Is Python a programming language? (yes/no): ").lower()
if answer == "yes":
    print("Correct answer!!")
    score += 1
else:
    print("Oops! Wrong answer!!")

answer = input("Which software controls computer hardware? ").lower()
if answer == "operating system":
    print("Correct answer!!")
    score += 1
else:
    print("Oops! Wrong answer!!")

answer = input("What does WWW stand for? ").lower()
if answer == "world wide web":
    print("Correct answer!!")
    score += 1
else:
    print("Oops! Wrong answer!!")

answer = input("Who created Python? ").lower()
if answer == "guido van rossum":
    print("Correct answer!!")
    score += 1
else:
    print("Oops! Wrong answer!!")


print("Total Score : ",score)
print(f"Percentage = {((score/7)*100):.2f}%")

