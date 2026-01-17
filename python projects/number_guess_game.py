import random
range = int(input("Enter top limit(only number) : \n"))
random_number = random.randrange(0,range)
guesses = 0
while True:
    guesses += 1
    guess = int(input("Make a guess(number only) : \n"))
    if guess == random_number:
        print("You got it!")
        break
    else:
        if guess > random_number:
            print("You were above the number")
        else:
            print("You were below the number..")
    
print(f"You got correct after {guesses} guesses.....:)\n")
        
    