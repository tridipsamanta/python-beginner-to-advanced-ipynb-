import pandas as pd
df = pd.DataFrame({
    'Value':[5,12,18,25,32,45,55,63,75,89]
})
print(df)
df['Equal_width_bin'] = pd.cut(df['Value'],bins=4)
print(df)