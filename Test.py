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

# Number of columns to apply formatting (first 3)
num_cols = 3  

# Create a copy for modifications
df_mod = df.copy()

for i in range(len(df)):
    # Excel rows are 1-based, pandas rows are 0-based
    excel_row = i + 2   # adjust if header rows exist in your file
    outline_level = ws.row_dimensions[excel_row].outlineLevel

    if outline_level > 0:
        for col in range(num_cols):
            val = df.iloc[i, col]
            if pd.notna(val):
                df_mod.iloc[i, col] = "-" * outline_level + " " + str(val).lstrip()

# Save back to Excel
df_mod.to_excel(output_path, index=False)

print(f"✅ Done! Updated sheet saved as: {output_path}")