import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any

# Function to query LLM for visualization
def generate_visualization_code(query: str, df: pd.DataFrame, llm) -> str:
    system_prompt = """
    You're an expert in generating Python code for visualizations using pandas and matplotlib.
    You will receive a user query and a dataframe with columns ready for visualization.
    Generate ONLY executable Python code to produce the required visualization, including axis labels, titles, legends, and any other necessary formatting clearly based on the provided query.
    Assume the DataFrame is named 'df' and do not include data loading, preprocessing, or any explanations.
    Always add plt.show() at the end.
    Do not include any additional text outside the executable code.
    """

    user_prompt = f"""
    User Query: {query}

    DataFrame columns: {list(df.columns)}

    Generate the Python matplotlib visualization code:
    """

    response = llm.invoke(system_prompt + user_prompt)

    code = response.content
    return code

# Main visualization function
def visualize_from_query(query: str, data: List[Dict[str, Any]], llm) -> None:
    """
    Generates and displays a matplotlib visualization based on a user's query and provided data.

    Args:
        query (str): The user's query describing the desired visualization.
        data (List[Dict[str, Any]]): A list of dictionaries convertible to a pandas DataFrame, each dictionary representing a row.
        llm: The language model interface used to generate executable visualization code.

    Returns:
        None. Directly executes visualization code to display the plot.
    """
    df = pd.DataFrame(data)
    visualization_code = generate_visualization_code(query, df, llm)

    print("Generated Visualization Code:")
    print(visualization_code)

    local_vars = {'df': df, 'pd': pd, 'plt': plt}
    try:
        exec(visualization_code, {}, local_vars)
    except Exception as e:
        print(f"Error executing generated code: {e}")

# Example Usage:
# visualize_from_query("Plot the sales trend over months with clear axes labels and a title.", data, llm)
