import pandas as pd
df = pd.DataFrame({
    'Value':[5,12,18,25,32,45,55,63,75,89]
})
print("Original Dataframe : ")
print(df)

bins = [0,40,70,100]
labels = ['low','medium','high']
df['custom_bins'] = pd.cut(df['Value'],bins=bins,labels=labels)
print('Custom Bining : ')
print(df)