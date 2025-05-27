prompt = """
You are given the first few rows of a pandas DataFrame where the header is multi-level (nested) across multiple rows. Your task is to:

1. Determine the correct header rows (usually the first 2 or 3 rows).
2. Combine the nested headers into univariate column names by concatenating them with an underscore `_`, or a space if more readable.
3. Replace missing or empty header cells with the most recent non-empty cell to their left in the same row.
4. Handle cases where a parent header spans multiple child headers. In such cases, propagate the parent label across all its spanned columns so that each child column gets a full combined name (e.g., if "FY22" spans 3 columns below it labeled "Sales", "Profit", "Expenses", then the final column names should be "FY22_Sales", "FY22_Profit", "FY22_Expenses").
5. Output the final flattened list of column names as they would appear in a cleaned DataFrame.

Example 1:
Input rows:
|        | 0      | 1        | 2      |
|--------|--------|----------|--------|
| 0      | Year 1 | Year 1   | Year 2 |
| 1      | Sales  | Profit   | Sales  |

Expected Output Column Names:
['Year 1_Sales', 'Year 1_Profit', 'Year 2_Sales']

Example 2:
Input rows:
|        | 0      | 1         | 2         | 3         |
|--------|--------|-----------|-----------|-----------|
| 0      | FY20   | FY20      | FY21      | FY21      |
| 1      | Sales  | Expenses  | Sales     | Profit    |

Expected Output Column Names:
['FY20_Sales', 'FY20_Expenses', 'FY21_Sales', 'FY21_Profit']

Example 3 (Parent spans multiple children):
Input rows:
|        | 0      | 1         | 2         | 3         | 4         |
|--------|--------|-----------|-----------|-----------|-----------|
| 0      | FY22   |           |           | FY23      |           |
| 1      | Sales  | Profit    | Expenses  | Sales     | Profit    |

Note: FY22 spans three columns: Sales, Profit, Expenses. FY23 spans two columns: Sales, Profit.

Expected Output Column Names:
['FY22_Sales', 'FY22_Profit', 'FY22_Expenses', 'FY23_Sales', 'FY23_Profit']

Now, here is a sample from a real DataFrame:

|        | 0         | 1             | 2         | 3         | ... |
|--------|------------|--------------|-----------|-----------|-----|
| 0      | FY20       | FY20         | FY20      | FY20      | ... |
| 1      | Sum of     | Sum of       | Sum of    | Sum of    | ... |
| 2      | Bill Amt   | P. Adv       | P. Bal    | Dis Amt   | ... |

Apply the same logic and generate a clean list of final column names.
"""