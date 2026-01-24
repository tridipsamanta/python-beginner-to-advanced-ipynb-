import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.DataFrame({
    'Text':[
        'Cats are running quickly',
        'Dogs are barking loudly',
        'They study in the university',
        'They are enjoying the holidays'
    ]
})

print('Original Dataframe : ')
print(df)

vecorizer = TfidfVectorizer()
x = vecorizer.fit_transform(df['Text'])
bow_df = pd.DataFrame(x.toarray(),columns=vecorizer.get_feature_names_out())
print('TF vectorizer .....')
print(bow_df)