#......Equal Width Bining.......
import pandas as pd

df = pd.DataFrame({
    'Value':[5,12,18,25,32,45,55,63,75,89]
})
print("Original Dataframe : ")
print(df)
df['equal_frequency_bin'] = pd.qcut(df['Value'],q=4)
print("After Equal frequency Bining : ")
print(df['equal_frequency_bin'])