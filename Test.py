import pandas as pd

# Define number of header rows at the top
num_header_rows = 3

# Extract header rows
header_rows = [tdf.iloc[i] for i in range(num_header_rows)]

# Create a DataFrame of headers and fill NaNs forward
header_df = pd.DataFrame(header_rows).T.fillna(method='ffill', axis=0)

# Combine headers with '_'
nested_headers = header_df.apply(lambda x: '_'.join(map(str, x)), axis=1).tolist()

# Output is a list of combined column names
print(nested_headers)