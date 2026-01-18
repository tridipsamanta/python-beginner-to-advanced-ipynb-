import random
# rock = 0, paper = 1 , scissors = 2
user_wins = 0
computer_wins = 0
options = ['rock','paper','scissors']
print("Welcome to (rock/paper/scissors) game Let's play 🥰🥰:)")
print("Rule : Whoever got 5 point first Wins ..🥳🥳🥳🥳")
while True:
    user = input("Enter (Rock/paper/scissors) or Q to quit : 🙂‍↔️ ").lower()
    if user == 'q':
        quit()
    if user not in ['rock','paper','scissors']:
        print("Please enter valid input next time..!🤬")
        continue
    random_number = random.randint(0,2)
    computer_pick = options[random_number]
    print("Computer picked : ",computer_pick)

    if user == 'scissors' and computer_pick == 'paper':
        user_wins += 1
        print("You win !! 🫣")
        continue
    elif user == 'rock' and computer_pick == 'scissors':
        user_wins += 1
        print("You Win !! 🫡")
        continue
    elif user == 'paper' and computer_pick == 'rock':
        user_wins += 1
        print("You wins !! 🤭")
        continue
    elif user == options[random_number]:
        print('Match Draw ! 😬')
        continue
    else:
        print('You lost..!🤧🤧')
        computer_wins += 1
    if user_wins == 5:
      print("Final Winner : (You)🤑🤠")
      print("Your Point : ",user_wins)
      print("Computer Point : ",computer_wins)
    elif computer_wins == 5:
        print("Final winner : (computer)🤖☠️☠️")
        print("Your Point : ",user_wins)
        print("Computer Point : ",computer_wins)
        break

print("Goodbye..!!")

    

