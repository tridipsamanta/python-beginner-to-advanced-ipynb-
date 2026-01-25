import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

data = {
    'Age':[20,30,40,50,np.nan],
    'Score':[90,40,60,np.nan,78],
    'Grade':['A','C','B',np.nan,'A']
}

df = pd.DataFrame(data)
print("Original dataframe : ")
print(df)

imputer = SimpleImputer(strategy='most_frequent')
df_imputed = pd.DataFrame(imputer.fit_transform(df[['Age','Score','Grade']]),columns=['Age','Score','Grade'])
df['Age'] = df_imputed['Age']
df['Score'] = df_imputed['Score']
df['Grade'] = df_imputed['Grade']

print("After mean calculation : ")
print(df)