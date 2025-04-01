import pandas as pd
import matplotlib.pyplot as plt

# Function to query LLM for visualization
def generate_visualization_code(query, df, llm):
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
def visualize_from_query(df, query, llm):
    visualization_code = generate_visualization_code(query, df, llm)

    print("Generated Visualization Code:")
    print(visualization_code)

    local_vars = {'df': df, 'pd': pd, 'plt': plt}
    try:
        exec(visualization_code, {}, local_vars)
    except Exception as e:
        print(f"Error executing generated code: {e}")

# Example Usage:
# visualize_from_query(df, "Plot the sales trend over months with clear axes labels and a title.", llm)
