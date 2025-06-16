import pandas as pd

# Let's say `tdf` is your DataFrame and header spans 5 rows
num_header_rows = 5

# Extract the header part and transpose
header_rows = [tdf.iloc[i] for i in range(num_header_rows)]
header_df = pd.DataFrame(header_rows).T

# Optional: Replace '%' or spaces with safe characters (if needed)
header_df = header_df.applymap(lambda x: str(x).strip().replace(' ', '_').replace('%', 'pct') if pd.notna(x) else x)

# Forward-fill *only when previous rows have non-null values* (to avoid misalignment)
for i in range(1, num_header_rows):
    header_df.iloc[:, i] = header_df.iloc[:, i].mask(header_df.iloc[:, i].isna(), header_df.iloc[:, i - 1])

# Combine non-null parts with underscore
def combine_parts(row):
    parts = [str(x).strip() for x in row if pd.notna(x) and str(x).strip().lower() != 'nan']
    return '_'.join(parts) if parts else 'unknown'

combined_headers = header_df.apply(combine_parts, axis=1).tolist()

# Print the corrected header list
print(combined_headers)