def is_pangram(text):
    text = text.lower()
    for ch in 'abcdefghijklmnopqrstuvwxyz':
        if ch not in text:
           return False
    return True

sentence = "The quick brown fox jumps over the lazy dog"
if is_pangram(sentence):
   print('Pangram')
else:
   print('Not pangram')