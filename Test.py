def build_system_prompt(tables: dict, query: str) -> str:
    """
    Builds a system prompt for ranking tables by their relevance to a query.

    Args:
        tables (dict): Dictionary of {table_name: [rows]}.
        query (str): The KPI-related query.

    Returns:
        str: A formatted system prompt string.
    """
    # Format tables into the required structure
    table_texts = []
    for idx, (table_name, rows) in enumerate(tables.items(), start=1):
        table_text = f"Table {idx} -> {table_name}\nRows: {rows}\n"
        table_texts.append(table_text)
    
    tables_section = "\n".join(table_texts)

    # System prompt
    system_prompt = f"""
You are an AI system that receives a query about a KPI (such as Revenue, EBITDA, Expenses, Miscellaneous Expenses, Refractive, Retina, etc.) 
and a set of tables. Each table will have a name and rows of data, formatted like this:

{tables_section}

Query:
{query}

Your task:
1. Carefully read the query and identify which table(s) are most relevant for answering it.
2. Rank all the given tables in order of probability of containing the answer to the query.
   - The first element in the ranked list must be the table name with the highest probability.
   - Continue ranking the remaining tables in descending order of probability.
3. Return only a Python list of table names, sorted by highest to lowest probability of containing the answer.

Be precise, logical, and consider table names as well as row contents when making your ranking.
Do not generate explanations—only output the ranked list of table names.
"""
    return system_prompt