from openpyxl import load_workbook
import pandas as pd

# Load workbook
wb = load_workbook("your_file.xlsx")
ws = wb.active

rows = []
for row in ws.iter_rows(values_only=False):  # keep formatting
    cell_value = row[1].value  # column B in your screenshot
    if cell_value is not None:
        indent = row[1].alignment.indent  # detect Excel indent level
        text = (" " * indent * 4) + str(cell_value)  # add 4 spaces per indent
        rows.append([text])

df = pd.DataFrame(rows, columns=["Revenue profile"])
print(df)