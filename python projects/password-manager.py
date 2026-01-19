from cryptography.fernet import Fernet

# def write_key():
#     key = Fernet.generate_key()
#     with open("key.key", "wb") as f:
#         f.write(key)

def load_key():
    with open("key.key", "rb") as f:
        return f.read()

# RUN ONCE, THEN COMMENT
# write_key()

key = load_key()
fer = Fernet(key)

def add():
    name = input("Account name: ")
    user_pwd = input("Password: ")

    encrypted = fer.encrypt(user_pwd.encode()).decode()

    with open("password.txt", "a") as f:
        f.write(name + "|" + encrypted + "\n")

    print("Password added succesfully !")

def view():
    with open('password.txt', 'r') as f:
        for line in f:
            if "|" in line:
                user, pwd = line.strip().split("|", 1)
                try:
                    decrypted = fer.decrypt(pwd.encode()).decode()
                    print("Username:", user, "Password:", decrypted)
                except:
                    print("Username:", user, "Password: <Invalid or Old Entry>")


while True:
    mode = input("would you like to add or veiw (add / view / q) : ").lower()

    if mode == 'q':
        break
    elif mode == 'add':
        add()
    elif mode == 'view':
        view()
    else:
        print("Invalid option")
