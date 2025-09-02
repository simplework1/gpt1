
import pandas as pd

def excel_to_dict(excel_path: str, sheet_name: str = None) -> dict:
    """
    Reads an Excel file and converts it into a dictionary where:
      - Keys are column headers
      - Values are lists of non-null values from that column
    Skips unnamed or fully NaN columns.

    Parameters:
        excel_path (str): Path to the Excel file.
        sheet_name (str, optional): Sheet name to read. 
                                    If None, the first sheet is used.
    """
    # If sheet_name is None, pandas will take the first sheet
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    result = {}
    for col in df.columns:
        # Ignore unnamed or fully empty columns
        if str(col).startswith("Unnamed") or df[col].dropna().empty:
            continue
        result[col] = df[col].dropna().tolist()

    return result


# Example usage:
# my_dict = excel_to_dict("Other expenses.xlsx")  # uses first sheet
# my_dict = excel_to_dict("Other expenses.xlsx", sheet_name="Synonyms")  # specific sheet
# print(my_dict)