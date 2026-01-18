print("                     👻 THE CURSED NIGHT ADVENTURE 👻 \n")
print("               Welcome... Only the brave will survive 😈 \n")

name = input("Type Your Name :) ")

print(f"\n           Hello {name}... The nightmare begins now...\n")

answer = input(
    "You wake up at midnight in a forgotten forest.\n"
    "Cold wind touches your neck. Trees whisper your name.\n"
    "Your phone is dead. The moon suddenly disappears.\n\n"
    "LEFT  – A broken house with flickering lights\n"
    "RIGHT – A foggy road leading to an old graveyard\n"
    "(left/right) : "
).lower()

# ================= LEFT PATH =================
if answer == "left":
    answer = input(
        "\nYou walk toward the broken house.\n"
        "The door opens slowly with a creaking sound.\n\n"
        "ENTER – Go inside the house\n"
        "KNOCK – Knock on the door\n"
        "(enter/knock) : "
    ).lower()

    if answer == "enter":
        answer = input(
            "\nInside the house, the walls are covered in blood marks.\n"
            "You hear footsteps upstairs.\n\n"
            "UPSTAIRS – Go upstairs\n"
            "HIDE     – Hide under the stairs\n"
            "(upstairs/hide) : "
        ).lower()

        if answer == "upstairs":
            answer = input(
                "\nUpstairs, you find a locked room.\n"
                "A girl is crying inside.\n\n"
                "OPEN – Break the door\n"
                "LISTEN – Listen carefully\n"
                "(open/listen) : "
            ).lower()

            if answer == "open":
                answer = input(
                    "\nThe door breaks open. The girl has no eyes.\n"
                    "She smiles at you.\n\n"
                    "RUN – Run away\n"
                    "STAY – Stay frozen\n"
                    "(run/stay) : "
                ).lower()

                if answer == "run":
                    print("\n🏃 You escape the house just in time.\n🏆 You survive (GOOD ENDING)")
                else:
                    print("\n👁️ She screams and steals your soul.\n💀 GAME OVER")

            else:
                answer = input(
                    "\nYou hear whispering: 'Help me leave this house'.\n\n"
                    "HELP – Agree to help\n"
                    "LEAVE – Ignore and leave\n"
                    "(help/leave) : "
                ).lower()

                if answer == "help":
                    print("\n🕯️ The spirit is freed.\n🏆 You escape safely (TRUE ENDING)")
                else:
                    print("\n👻 The house collapses on you.\n💀 GAME OVER")

        else:
            answer = input(
                "\nYou hide silently. A shadow walks past you.\n\n"
                "FOLLOW – Follow the shadow\n"
                "WAIT   – Stay hidden\n"
                "(follow/wait) : "
            ).lower()

            if answer == "follow":
                print("\n👹 The shadow notices you.\n💀 You are dragged into darkness (GAME OVER)")
            else:
                print("\n⏳ The shadow disappears.\n🏆 You escape (NEUTRAL ENDING)")

    else:
        answer = input(
            "\nNo one answers. Suddenly, the door opens itself.\n\n"
            "ENTER – Enter quickly\n"
            "RUN   – Run away\n"
            "(enter/run) : "
        ).lower()

        if answer == "enter":
            print("\n🩸 The door slams shut.\n💀 You are trapped forever (GAME OVER)")
        else:
            print("\n🏃 You run back to the forest.\n🏆 You survive (SAFE ENDING)")

# ================= RIGHT PATH =================
elif answer == "right":
    answer = input(
        "\nYou walk toward the graveyard.\n"
        "Graves are shaking. A bell rings by itself.\n\n"
        "LOOK – Look at the graves\n"
        "PRAY – Pray silently\n"
        "(look/pray) : "
    ).lower()

    if answer == "look":
        answer = input(
            "\nOne grave is open.\n"
            "A hand reaches out.\n\n"
            "PULL – Pull the hand\n"
            "STEP – Step back\n"
            "(pull/step) : "
        ).lower()

        if answer == "pull":
            answer = input(
                "\nA ghost rises from the grave.\n"
                "'Finish my ritual,' it says.\n\n"
                "AGREE – Help the ghost\n"
                "REFUSE – Refuse\n"
                "(agree/refuse) : "
            ).lower()

            if answer == "agree":
                print("\n🕯️ The ritual is complete.\n🏆 Ghost blesses you (BEST ENDING)")
            else:
                print("\n☠️ The ghost drags you underground.\n💀 GAME OVER")
        else:
            print("\n⚰️ The ground collapses.\n💀 You fall into darkness (GAME OVER)")

    else:
        answer = input(
            "\nWhile praying, you hear footsteps behind you.\n\n"
            "TURN – Turn around\n"
            "IGNORE – Keep praying\n"
            "(turn/ignore) : "
        ).lower()

        if answer == "turn":
            print("\n👹 A demon stands behind you.\n💀 GAME OVER")
        else:
            print("\n🙏 The footsteps fade away.\n🏆 You survive (FAITH ENDING)")

print("\nThanks for playing... Sleep well tonight 😈")
