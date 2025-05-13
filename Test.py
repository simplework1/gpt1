import pandas as pd

def split_excel_sheet_to_tables(file_path, sheet_name=0, threshold=2):
    """
    Reads an Excel sheet and splits it into multiple tables based on blank rows.
    
    :param file_path: Path to the Excel file
    :param sheet_name: Sheet name or index to read from
    :param threshold: Max number of non-NaN cells in a row to consider it a separator
    :return: List of DataFrames, each representing a separate table
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Find blank or near-blank rows
    blank_rows = df.apply(lambda row: row.count() <= threshold, axis=1)

    # Split indexes
    table_indices = []
    start_idx = None

    for i, is_blank in enumerate(blank_rows):
        if not is_blank and start_idx is None:
            start_idx = i
        elif is_blank and start_idx is not None:
            table_indices.append((start_idx, i))
            start_idx = None
    if start_idx is not None:  # Handle last table
        table_indices.append((start_idx, len(df)))

    # Extract DataFrames
    tables = [df.iloc[start:end].reset_index(drop=True) for start, end in table_indices]
    
    return tables