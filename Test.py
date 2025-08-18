import openpyxl

def format_kpi_value(kpi_name, value_dict):
    """
    Converts a dict like:
    {"FY22": "2648.55 INR in millions", "FY23": "3666.92 INR in millions"}
    into a formatted string with KPI name at the top.
    """
    if not isinstance(value_dict, dict):
        return str(value_dict)

    lines = []
    first_val = next(iter(value_dict.values()))  # first available value
    lines.append(f"{kpi_name} : {first_val}")
    
    for period, val in value_dict.items():
        lines.append(f"{period} : {val}")
    
    return "\n".join(lines)

def fill_excel_template(file_path, sheet_name, value_dict, output_path):
    wb = openpyxl.load_workbook(file_path)
    
    if sheet_name not in wb.sheetnames:
        raise ValueError(f"Sheet '{sheet_name}' not found in workbook")
    
    ws = wb[sheet_name]

    def normalize(s):
        return str(s).strip().lower() if s else ""

    # Step 1: Detect the header row (column headers)
    header_row_idx = None
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        values = [normalize(c.value) for c in row if c.value]
        if sum(normalize(k) in values for k in value_dict.keys()) >= 1:
            header_row_idx = row[0].row
            break
    if not header_row_idx:
        raise ValueError("Could not detect column headers in template!")

    # Step 2: Detect the header column (row headers)
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
        cell = row[header_col_idx - 1]
        if cell.value:
            row_headers[normalize(cell.value)] = cell.row

    # Step 4: Fill values
    for company, kpis in value_dict.items():
        company_key = normalize(company)
        if company_key not in col_headers:
            continue
        col_idx = col_headers[company_key]

        for kpi, val in kpis.items():
            kpi_key = normalize(kpi)
            if kpi_key not in row_headers:
                continue
            row_idx = row_headers[kpi_key]

            # If dict, format into string
            if isinstance(val, dict):
                val = format_kpi_value(kpi, val)

            ws.cell(row=row_idx, column=col_idx, value=val)

    wb.save(output_path)
    print(f"Template filled and saved to {output_path}")