import pandas as pd
data = {
    'A':[1,2,2,3,3,4],
    'B':[5,6,6,7,8,8]
}

df = pd.DataFrame(data)
print("Original Dataframe : ")
print(df.to_string(index=False))
print("Duplicates rows : ")
print(df[df.duplicated(subset=['A'])].to_string(index=False))
df.drop_duplicates(subset=['A'],keep='first',inplace=True)
print("Dataframe after removing duplicates based on column 'A' :")
print(df.to_string(index=False))