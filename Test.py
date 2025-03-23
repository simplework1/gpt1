import pandas as pd
from pandasai import SmartDataframe

# Sample DataFrame
data = {'col1': [1, 2, 3, 4, 5],
        'col2': ['A', 'B', 'C', 'D', 'E'],
        'col3': [10.5, 12.3, 14.7, 11.2, 13.8]}
df = pd.DataFrame(data)

# Custom DataFrame description
df_description = "This DataFrame contains numerical and categorical data about various items."

# Custom column descriptions
column_descriptions = {
    "col1": "A numerical identifier for each item.",
    "col2": "A categorical label representing the item's category.",
    "col3": "A numerical value representing the item's measurement."
}

# Initialize SmartDataframe with descriptions
sdf = SmartDataframe(df, config={"df_description": df_description, "column_descriptions": column_descriptions})

# Now you can use pandasai with your custom descriptions
print(sdf.chat("What is the average of col1?"))

print(sdf.chat("Describe the distribution of col3."))

print(sdf.chat("What are the unique values in col2?"))