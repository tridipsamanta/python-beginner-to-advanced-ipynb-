def remove_nth_char(text,n):
    result = " "
    for i in range(len(text)):
        if i != n:
            result = result + text[i]

    return result  
word = input("Enter any word : ")
n = int(input("Enter nth digit to remove : "))
print(remove_nth_char(word,n))
