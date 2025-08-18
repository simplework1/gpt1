import openpyxl

def fill_excel_template(file_path, value_dict, output_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    def normalize(s):
        return str(s).strip().lower() if s else ""

    # Step 1: Detect the header row (where col headers like Route/Oslo appear)
    header_row_idx = None
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        values = [normalize(c.value) for c in row if c.value]
        # Assume header row must contain at least 2 company names from dict
        if sum(normalize(k) in values for k in value_dict.keys()) >= 1:
            header_row_idx = row[0].row
            break

    if not header_row_idx:
        raise ValueError("Could not detect column headers in template!")

    # Step 2: Detect the header column (where KPIs like Cataract/Retina appear)
    header_col_idx = None
    for col in ws.iter_cols(min_col=1, max_col=ws.max_column):
        values = [normalize(c.value) for c in col if c.value]
        if any(normalize(kpi) in values for comp in value_dict.values() for kpi in comp.keys()):
            header_col_idx = col[0].column
            break

    if not header_col_idx:
        raise ValueError("Could not detect row headers in template!")

    # Step 3: Build header mappings
    col_headers = {}
    for cell in ws[header_row_idx]:
        if cell.col_idx >= header_col_idx and cell.value:
            col_headers[normalize(cell.value)] = cell.col_idx

    row_headers = {}
    for row in ws.iter_rows(min_row=header_row_idx + 1, max_row=ws.max_row):
        cell = row[header_col_idx - 1]  # KPI names
        if cell.value:
            row_headers[normalize(cell.value)] = cell.row

    # Step 4: Fill values
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

    wb.save(output_path)
    print(f"Template filled and saved to {output_path}")