from openpyxl import load_workbook

file_path = "your_file.xlsx"
sheet_name = "Other expense"
output_path = "formatted_output.xlsx"

# Load workbook and target sheet
wb = load_workbook(file_path)
ws = wb[sheet_name]

# Helper: safe conversion to float
def to_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

# Iterate rows
for row in range(1, ws.max_row + 1):
    outline_level = ws.row_dimensions[row].outlineLevel

    # Process only parent rows (outline level == 0)
    if outline_level == 0:
        # Find child rows until next parent
        child_row = row + 1
        while child_row <= ws.max_row and ws.row_dimensions[child_row].outlineLevel > 0:
            child_row += 1

        # If children exist, aggregate
        if child_row > row + 1:
            for col in range(2, ws.max_column + 1):  # skip first col (labels)
                parent_val = to_float(ws.cell(row=row, column=col).value)
                child_sum = 0.0
                has_child_number = False

                # sum only children (no parent included)
                for r in range(row + 1, child_row):
                    val = to_float(ws.cell(row=r, column=col).value)
                    if val is not None:
                        child_sum += val
                        has_child_number = True

                if has_child_number:
                    if parent_val is None:
                        # Parent empty → replace with sum
                        ws.cell(row=row, column=col).value = child_sum
                    else:
                        # Compare parent with child sum
                        if parent_val < child_sum:
                            ws.cell(row=row, column=col).value = child_sum
                        else:
                            ws.cell(row=row, column=col).value = parent_val

# Save updated workbook
wb.save(output_path)

print(f"✅ Aggregation with comparison complete! Updated file saved as: {output_path}")