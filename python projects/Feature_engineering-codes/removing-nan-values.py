import pandas as pd

data = {
    'A':[1,2,None,4,5],
    'B':[None,2,3,4,5],
    'C':[1,2,3,4,None]
}

df = pd.DataFrame(data)
print("Original DataFrame : ")
print(df)

df_cleaned = df.dropna()
print("After Removing Nan values : ")
print(df_cleaned)