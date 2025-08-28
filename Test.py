import pandas as pd

# assume your DataFrame is called df

# Find index of row where 'sum' appears as substring in the first column (ignore case)
idx = df[df.iloc[:, 0].astype(str).str.contains('sum', case=False, na=False)].index

if not idx.empty:
    cutoff = idx[0]   # first occurrence
    df_trimmed = df.loc[:cutoff]   # keep everything including that row
else:
    df_trimmed = df.copy()  # if no match, keep entire df

print(df_trimmed)