import pandas as pd
from openpyxl import load_workbook

# Path to your Excel file
file_path = "your_file.xlsx"

# Load workbook with openpyxl
wb = load_workbook(file_path)
ws = wb["Other expense"]  # Select the specific sheet

categories = []

# Loop through rows of first column
for row in ws.iter_rows(min_row=1, max_col=1):
    cell = row[0]
    val = cell.value
    
    if val is not None:
        outline_level = ws.row_dimensions[cell.row].outlineLevel
        if outline_level > 0:  # Subcategory
            categories.append("-" * outline_level + " " + str(val))
        else:  # Main category
            categories.append(str(val))
    else:
        categories.append(None)

# Load Excel into pandas (specific sheet)
df = pd.read_excel(file_path, sheet_name="Other expense")

# Replace first column with modified categories
df.iloc[:, 0] = categories

# Save formatted output
df.to_excel("formatted_output.xlsx", index=False, sheet_name="Other expense")

print("✅ Done! Check 'formatted_output.xlsx'")