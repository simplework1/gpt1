from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool

# Step 1: Connect to your database
db = SQLDatabase.from_uri("sqlite:///your_database.db")

# Step 2: Customize table schema information
def custom_get_table_info(self, table_names=None):
    """Returns table schema including column descriptions."""
    table_info = self.get_table_info_no_description(table_names)
    # Add column descriptions manually
    table_info += """
    Descriptions:
    - users (id: Unique ID, name: Full Name, email: Contact Email)
    - orders (id: Order ID, user_id: Reference to users.id, amount: Order Amount)
    """
    return table_info

# Override the method
SQLDatabase.get_table_info = custom_get_table_info

# Step 3: Create SQL Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db),
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Step 4: Run Queries
query = "What are the total order amounts for each user?"
response = agent.run(query)
print(response)