import os
DATA_FILE = "data.txt"

#load existing expenses
def load_expenses():
    expenses = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|")

                if(len(parts)) != 3:
                 continue
                amount,category,note = parts
                expenses.append({
                    "amount":float(category),
                    "category":category,
                    "note":note
                })
    return expenses

#save expenses
# def save_expenses(expenses):
#     with open("DATA_FILE","w") as f:
#         for e in expenses:
#             f.write(f"{e["amount"]}|{["category"]}|{e["note"]}\n")

def single_expenses(expenses):
    with open(DATA_FILE,'a') as f :
        f.write(f"{expenses['amount']}|{expenses['category']}|{expenses['note']}\n")

#add expenses
def add_expenses(expenses):
    amount = float(input("Enter amount : "))
    category = input("Enter category (food, travel, shopping, etc) : ")
    note = input("Any note : ")

    expenses = ({
        "amount":amount,
        "category":category,
        "note":note
    })     

    expenses.append(expenses)

    save_expenses(expenses)
    print("Expenses added successfully!")

#view expenses 
def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet..")
        return
    print("\n---  All Expenses ---")
    for e in expenses:
        print(f"{e['amount']} INR - {e['category']} - {e['note']}")

#view total spending
def view_total(expenses):
    total = sum(e["amount"] for e in expenses)
    print(f"\n Total spending : {total} INR")

#category - wise summary
def view_category_summary(expenses):
    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"],0) + e["amount"]

    print("\n--- Category-wise Spending ---")
    for cat,total in category_totals.items():
        print(f"{cat}:{total} INR")

#main menu set-up
def main():
    expenses = load_expenses()

    while True:
        print("\n ==== PERSONAL BUDGET TRACKER ====")
        print("1. Add expenses")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. View category-wise Summary")
        print("5. exit")
        choice = input("Enter choice : ")

        if choice == "1":
            add_expenses(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_total(expenses)
        elif choice == "4":
            view_category_summary(expenses)
        elif choice == "5":
            print("Exiting .....Goodbye!")
            break
        else:
            print("Invalid Choice, try again!")
main()   