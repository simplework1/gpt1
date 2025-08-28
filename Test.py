import pandas as pd

# assume your DataFrame is called df
# and you want to check the first column

# Find index of row where 'Sum' occurs
idx = df[df.iloc[:, 0].str.strip().str.lower() == 'sum'].index

if not idx.empty:
    cutoff = idx[0]   # first occurrence
    df_trimmed = df.loc[:cutoff]   # keep everything including "Sum"
else:
    df_trimmed = df.copy()  # if "Sum" not found, keep whole df

print(df_trimmed)