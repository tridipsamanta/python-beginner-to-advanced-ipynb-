import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
data = pd.DataFrame({
    'Text':[
        'Cats are running quickly',
        'Dogs are barking loudly',
        'They study in the university',
        'They are enjoying the holidays'
    ]
})

print("Original Dataframe : ")
print(data)

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(data['Text'])
bow_df = pd.DataFrame(x.toarray(),columns=vectorizer.get_feature_names_out())
print("Bag of Words : ")
print(bow_df)