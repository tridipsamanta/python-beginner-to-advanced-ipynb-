# caffe order management system ..........
import pandas as pd
print("Welcome to my Restrurent . Here's the menu ....")
menu = {
    'pizza':350,
    'pasta':80,
    'burger':50,
    'salad':60,
    'coffe':50
}
print("Pizza:350\nPasta :80\nBurger :50\nGreen Salad :60\nCoffe :50")
order_total = 0
item_1 = input('Enter the name of item you want to order :) ').lower()

while True:
    if item_1 in menu:
        order_total += menu[item_1]
        print(f'Your {item_1} has been added Sucsessfully.')
    else:
        print(f'please enter a valid Item name ')
    another_item = input('Do you order another item ? (yes/no) : ').lower()
    if another_item == 'yes':
        item_2 = input('Enter the item name you want to add : ').lower()
        if item_2 in menu:
            order_total += menu[item_2]
            print(f'Ordered {item_2} succsesfully.')
        else:
            print(f'Please enter a valid item name :) ')
    else:
         print('Thank you :) ')
         break

print('Your Total bill : ',order_total)
