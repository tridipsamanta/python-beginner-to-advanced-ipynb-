import pandas as pd

from category_encoders import TargetEncoder

data = pd.DataFrame({
    'Fruit':['banana','apple','orrange','apple','mango'],
    'Color':['red','blue','green','red','black']
})

print('Original dataframe : ')
print(data)

labelencoder = TargetEncoder(cols=['Fruit','Color'])

data_encoded = data.copy()

data_encoded[['Fruit','Color']] = labelencoder.fit_transform(data[['Fruit','Color']],data['Fruit'])
print('After lebel encoding : ')
print(data_encoded)