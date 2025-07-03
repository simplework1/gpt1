import os
import re
from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# --- 1. Define Tools ---

@tool
def detect_city_scope(question: str) -> str:
    """
    Determines whether the user input references a single city or multiple.
    Returns 'single' or 'multiple' along with detected city names.
    """
    known_cities = ["paris", "tokyo", "london", "new york", "berlin", "madrid"]
    found = []
    for city in known_cities:
        if re.search(rf"\b{re.escape(city)}\b", question, re.IGNORECASE):
            found.append(city)
    if not found:
        return "none | []"
    elif len(found) == 1:
        return f"single | {found}"
    else:
        return f"multiple | {found}"


@tool
def get_weather(city: str) -> str:
    """Gets the current weather for a specified city."""
    print(f"--- Calling Tool: get_weather(city='{city}') ---")
    city_lower = city.lower()
    if "paris" in city_lower:
        return "The weather in Paris is 20°C and sunny."
    elif "tokyo" in city_lower:
        return "The weather in Tokyo is 25°C and humid."
    elif "london" in city_lower:
        return "The weather in London is 18°C and cloudy."
    else:
        return f"Sorry, I don't have weather information for {city}."


@tool
def generate_outfit_suggestion(weather_info: str) -> str:
    """Generates an outfit suggestion based on weather info."""
    print(f"--- Calling Tool: generate_outfit_suggestion(weather_info='{weather_info}') ---")
    info = weather_info.lower()
    if "sunny" in info:
        return "It's sunny! A t-shirt, shorts, and sunglasses would be perfect."
    elif "humid" in info:
        return "It's humid. Wear something light and breathable, like linen pants."
    elif "cloudy" in info:
        return "It's cloudy. A hoodie and jeans would be a good choice."
    else:
        return "A general outfit of jeans and a light jacket would be suitable."


# --- 2. Prompt Template with City Scope Step Included ---

prompt_template = """
You are a helpful assistant that suggests outfits based on the weather. Follow these steps strictly:

1. First, use the `detect_city_scope` tool to determine if the user input mentions one or multiple cities.
2. If the result is "single", proceed to:
    - Use the `get_weather` tool to get the weather for the city.
    - Use the `generate_outfit_suggestion` tool with that weather info.
3. If the result is "multiple", REPHRASE the original input into one question per city, and handle each separately in a loop. You MUST return combined outfit suggestions at the end, one per city.
4. Do not call `get_weather` or `generate_outfit_suggestion` before using `detect_city_scope`.

Here are the tools you can use:
{tools}

Format your response like this:

Thought: Do I need to use a tool? Yes
Action: tool_name
Action Input: the input to the tool
Observation: result of the tool

At the end, when done for all cities:
Thought: I now have the final answer.
Final Answer: [full combined outfit suggestions here]

User Input: {input}
Thought:
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(prompt_template)

# --- 3. Setup Agent ---

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [detect_city_scope, get_weather, generate_outfit_suggestion]
agent_executor = create_react_agent(llm, tools, messages_modifier=prompt)

# --- 4. Run Agent ---

def run_agent(user_input: str):
    print(f"\n🧠 Running ReAct agent for: \"{user_input}\"\n")
    inputs = {"messages": [HumanMessage(content=user_input)]}

    for s in agent_executor.stream(inputs, stream_mode="values"):
        if "logs" in s:
            print(s["logs"])
        elif "messages" in s:
            print("--- Final Response ---")
            s["messages"][-1].pretty_print()

    final_state = agent_executor.invoke(inputs)
    print("\n✅ Final Answer:")
    print(final_state["messages"][-1].content)


# --- 5. Main Runner ---

if __name__ == "__main__":
    question = "What should I wear in Paris and London?"
    run_agent(question)