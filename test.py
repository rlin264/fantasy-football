import pandas as pd

df = pd.DataFrame({'a':[1,2], 'b':[3,4]})
df['c'] = df.apply(lambda row: row.a + row.b, axis=1)
print(df)