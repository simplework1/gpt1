
import re

# Sample string (from your image)
text = """
Relevancy    Relevant


Reason : The article talks about xyz.
"""

# Define regex to extract 'Relevancy' and 'Reason'
pattern = r"Relevancy\s+(.*?)\n+\s*Reason\s*:\s*(.+)"

# Apply regex
match = re.search(pattern, text, re.DOTALL)  # Use re.DOTALL to capture multiline content
if match:
    result = {
        "Relevancy": match.group(1).strip(),
        "Reason": match.group(2).strip()
    }
    print(result)
else:
    print("No match found!")