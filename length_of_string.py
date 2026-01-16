def string_length(s):
    count = 0
    for i in s:
        count += 1
    return count
    
text = input("Enter a String : ")
print(string_length(text))