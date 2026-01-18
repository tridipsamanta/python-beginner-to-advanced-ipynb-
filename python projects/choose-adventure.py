print("                           🌲 The Forgotten Forest Adventure :) \n")
print("                     Let's Play :) \n")

name = input("Type Your Name :) ")

print(f"                Welcome {name} Let's Start :)  ")

answer = input("You wake up in a dark forest. The trees are tall, the air is cold, and you hear strange sounds." \
" A mysterious voice whispers your name and says: " \
"LEFT – A narrow path with glowing blue mushrooms" \
"RIGHT – A wide path leading into deep darkness (left/right) : ").lower()

if answer == 'left':
    answer = input("You walk carefully along the glowing path. After a while, you reach a quiet river." \
    "The river is flowing fast, and you must decide how to cross it." \
    "SWIM – Jump into the cold water" \
    "BRIDGE – Use an old wooden bridge (swim/bridge) : ").lower()
    if answer == 'swim':
        answer = input("The water is freezing and the current is strong." \
        "You struggle but manage to reach the other side." \
        "On the shore, you see a shiny sword stuck in a stone." \
        "PULL – Try to pull the sword out" \
        "IGNORE – Walk away (pull/ignore) : ").lower()
        if answer == 'pull':
            print("The sword comes out easily. You feel powerful. 🏆 You become the Guardian of the Forest (WIN)")
             
        else:
            print("A wild beast attacks you from behind.💀 You did not survive (GAME OVER)")
    else:
        answer = input("The bridge creaks as you step on it.Halfway through, it breaks.You fall into the river." \
    "💀 You drowned (GAME OVER)")

elif answer == 'right':
    answer = input("You walk into the darkness.Suddenly, you see a cave with firelight inside." \
    "ENTER – Go inside the cave" \
    "RUN – Run away into the forest (enter/run) :) ").lower()
    if answer == 'enter':
        answer = input("STEAL – Try to steal the gold" \
        "SNEAK – Quietly leave the cave (steal/sneak) :) ").lower()
        if answer == 'steal':
            print("The dragon wakes up and breathes fire.💀 You were burned (GAME OVER)")
        else:
            print("You escape safely and find a hidden exit.🏆 You survive with wisdom (WIN)")
    else:
        answer = input("You run blindly and fall into a deep pit.💀 You fell into a trap (GAME OVER)")
        

print("Goodbye...")


