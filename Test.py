prompt = """
You are given an HTML table that may have:
- Nested column headers (<thead> with multiple <tr> levels using rowspan and colspan)
- Row headers on the left (e.g., in the first <td>/<th> cells of <tbody> rows)
- A bivariate structure, where both row and column headers define the meaning of a data cell

Your task is to:

1. Parse the entire HTML table, including nested <thead> and <tbody> or <tfoot>.
2. Flatten and combine column headers into a single label using a separator like " - " (e.g., "Revenue - FY24").
3. Flatten and combine row headers the same way, if present.
4. Based on the structure:
   - If the table is univariate (only column headers), return an array of row objects.
   - If the table is bivariate (row and column headers), return a nested JSON object, where row headers form keys at one level, and column headers form keys at the next.

Output Requirements:
- Output valid JSON only.
- Use appropriate numeric or string values as per table content.
- Do not include HTML, markdown, or explanations—only the JSON.

Input HTML:
(Insert HTML table here)

Output Format Examples:

For univariate table:

[
  {
    "Procedure": "Cataract",
    "Revenue - FY23": 30.97,
    "Revenue - FY24": 53.31
  }
]

For bivariate table:

{
  "Cataract": {
    "Revenue - FY23": 30.97,
    "Revenue - FY24": 53.31
  },
  "Lasik": {
    "Revenue - FY23": 10.12,
    "Revenue - FY24": 15.50
  }
}
"""