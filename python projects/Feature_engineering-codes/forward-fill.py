import numpy as np
import pandas as pd
data = {
    'Age':[20,30,40,50,np.nan],
    'Score':[90,40,60,np.nan,78],
    'Grade':['A','C','B','C','A']
}

df = pd.DataFrame(data)
print("Original dataframe : ")
print(df)

df_forward_fill = df.fillna(method='ffill')

print("Forward Fill : ")
print(df_forward_fill)

