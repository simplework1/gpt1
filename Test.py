import openpyxl

def fill_excel_template(file_path, value_dict, output_path):
    # Load workbook and active sheet
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    # Normalize headers (case-insensitive)
    def normalize(s):
        return str(s).strip().lower() if s else ""

    # Find row headers (first column with text values like Cataract, Refractive...)
    row_headers = {}
    col_headers = {}

    # Build mapping of row headers
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        cell = row[0]  # first column is row header
        if cell.value:
            row_headers[normalize(cell.value)] = cell.row

    # Build mapping of column headers
    for col in ws.iter_cols(min_col=2, max_col=ws.max_column):  
        cell = col[0]  # first row is column header
        if cell.value:
            col_headers[normalize(cell.value)] = cell.column

    # Fill values from dict
    for company, kpis in value_dict.items():
        company_key = normalize(company)
        if company_key not in col_headers:
            continue

        col_idx = col_headers[company_key]

        for kpi, value in kpis.items():
            kpi_key = normalize(kpi)
            if kpi_key not in row_headers:
                continue

            row_idx = row_headers[kpi_key]
            ws.cell(row=row_idx, column=col_idx, value=value)

    # Save to output path
    wb.save(output_path)
    print(f"Template filled and saved to {output_path}")