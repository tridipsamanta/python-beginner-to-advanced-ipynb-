letter = '''
    Dear <|Name|>
       you are selected!
       <|Date|>
'''
print(letter.replace("<|Name|>","tridip").replace("<|Date|>","4 june 2025"))