import pandas as pd

data = {
    'A':[1,2,3,None,5],
    'B':[1,None,3,4,5],
    'C':[1,2,None,None,5]
}

df = pd.DataFrame(data)

print("Original Dataframe : \n",df)
df.fillna(0,inplace=True)
print("After filling Nan with 0 : \n",df)