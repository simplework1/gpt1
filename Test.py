from openpyxl import load_workbook

file_path = "your_file.xlsx"
sheet_name = "Other expense"
output_path = "formatted_output.xlsx"

# Load workbook and target sheet
wb = load_workbook(file_path)
ws = wb[sheet_name]

# Loop through all rows and all columns with values
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
    for cell in row:
        if cell.value is None:
            continue

        # Get outline level for this row
        outline_level = ws.row_dimensions[cell.row].outlineLevel

        if outline_level > 0:
            # Add prefix only if not already prefixed
            if not str(cell.value).startswith("-"):
                cell.value = "-" * outline_level + " " + str(cell.value)

# Save updated workbook
wb.save(output_path)

print(f"✅ Done! Prefixed grouped rows directly in Excel → {output_path}")