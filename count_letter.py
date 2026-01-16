def count_letter(s,letter):
    if not s:
        return 0
    return (s[0] == letter)+ count_letter(s[1:],letter)

text = input("Enter a String : ")
letter = input("Enter a letter to count : ")

print(count_letter(text,letter))
