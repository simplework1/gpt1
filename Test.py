    # Step 3: Build header mappings (take first occurrence only)
    col_headers = {}
    for cell in ws[header_row_idx]:
        if cell.col_idx >= header_col_idx and cell.value:
            key = normalize(cell.value)
            if key not in col_headers:   # ✅ only take first occurrence
                col_headers[key] = cell.col_idx

    row_headers = {}
    for row in ws.iter_rows(min_row=header_row_idx + 1, max_row=ws.max_row):
        cell = row[header_col_idx - 1]  # KPI name cell
        if cell.value:
            key = normalize(cell.value)
            if key not in row_headers:  # ✅ only take first occurrence
                row_headers[key] = cell.row