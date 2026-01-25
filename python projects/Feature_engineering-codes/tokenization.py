
import pandas as pd
from nltk.tokenize import word_tokenize

import nltk 
nltk.download('punk_tab')

df = pd.DataFrame({
    'Text':[
        'Cats are running quickly',
        'Dogs are barking loudly',
        'They study in the university',
        'They are enjoying the holidays'
    ]
})
print("Original dataframe : ")
print(df)

df['tokens'] = df['Text'].apply(lambda x : word_tokenize(x.lower()))
print("After tokeinzation : ")
print(df[['Text','tokens']])
