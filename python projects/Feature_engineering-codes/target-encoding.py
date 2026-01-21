import pandas as pd

from category_encoders import TargetEncoder

data = {
    'Fruit':['Apple','Banana','Orange','Apple','Banana'],
    'Color':['Red','Yellow','Orange','Green','Yellow']
}
df = pd.DataFrame(data)
print("Original Dataset : ")
print(df)

target_encoder = TargetEncoder(cols=['Fruit','Color'])
df_target_encoded = df.copy()
df_target_encoded[['Fruit','Color']] = target_encoder.fit_transform(df[['Fruit','Color']],df['Fruit'])
print("\n After Target Encoding : ")
print(df_target_encoded)
