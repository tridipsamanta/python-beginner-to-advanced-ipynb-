def remove_odd_index(text):
    result = " "
    for i in range(len(text)):
        if i%2==0:
            result = result + text[i]
    return result

word = input("Enter any  word : ")
print(remove_odd_index(word))