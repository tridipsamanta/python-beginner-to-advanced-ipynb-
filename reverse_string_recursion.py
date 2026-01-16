def reverse_recursive(s):
    if len(s) == 0:
        return s
    return reverse_recursive(s[1:]) + s[0]
text = input("Enter a word : ")
print(reverse_recursive(text))