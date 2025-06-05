import pandas as pd

# Load the Excel file
file_path = 'your_file.xlsx'  # Change this to your Excel file path
df = pd.read_excel(file_path, header=None)

# Extract row and column headers
row_headers = df.iloc[1:, 0].tolist()       # All rows from second row, first column
col_headers = df.iloc[0, 1:].tolist()       # First row, all columns from second column

# Initialize the nested dictionary
my_dict = {}

# Iterate through rows and columns to populate the dictionary
for i, row_header in enumerate(row_headers):
    my_dict[row_header] = {}
    for j, col_header in enumerate(col_headers):
        value = df.iat[i + 1, j + 1]  # +1 to skip headers
        my_dict[row_header][col_header] = value

# Optional: print the dictionary
# import pprint; pprint.pprint(my_dict)