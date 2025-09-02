import pandas as pd
from openpyxl import load_workbook

file_path = "your_file.xlsx"
sheet_name = "Other expense"
output_path = "formatted_output.xlsx"

# Load workbook + specific sheet
wb = load_workbook(file_path, data_only=True)
ws = wb[sheet_name]

# Load data into pandas
df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

# Create a new list for first column
categories = []

for i in range(len(df)):
    excel_row = i + 2  # pandas skips the first row, Excel is 1-based (adjust this if needed!)
    cell_value = df.iloc[i, 0]

    if pd.isna(cell_value):  # Skip empty labels
        categories.append(cell_value)
        continue

    outline_level = ws.row_dimensions[excel_row].outlineLevel

    if outline_level > 0:
        categories.append("-" * outline_level + " " + str(cell_value))
    else:
        categories.append(str(cell_value))

# Replace the first column with modified categories
df.iloc[:, 0] = categories

# Save back to Excel
df.to_excel(output_path, index=False)

print(f"✅ Done! Updated sheet saved as: {output_path}")