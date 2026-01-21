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
df_backward_fill = df.fillna(method='bfill')
print("Backward fill : ")
print(df_backward_fill)