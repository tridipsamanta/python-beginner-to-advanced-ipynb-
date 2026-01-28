import pandas as pd
from sklearn.preprocessing import OneHotEncoder
data = {
    'Fruit':['Apple','Banana','Orange','Apple','Banana'],
    'Color':['Red','Yellow','Orange','Green','Yellow']
}

df = pd.DataFrame(data)
print('original dataframe : ')
print(df)

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(df)
df_encoded = pd.DataFrame(encoded,columns=encoder.get_feature_names_out())
print(df_encoded)