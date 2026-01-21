import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer

data = {
    'Age':[20,30,40,50,np.nan],
    'Score':[90,40,60,np.nan,78],
    'Grade':['A','C','B','C','A']
}

df = pd.DataFrame(data)
print("Original dataframe : ")
print(df)

imputer = SimpleImputer(strategy='median')
df_imputed = pd.DataFrame(imputer.fit_transform(df[['Age','Score']]),columns=['Age','Score'])
df['Age'] = df_imputed['Age']
df['Score'] = df_imputed['Score']

print("After mean calculation : ")
print(df)