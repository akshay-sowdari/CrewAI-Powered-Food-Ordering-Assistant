from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv("OPENAI_API_KEY"))
from langchain_openai import OpenAI
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import random
import re

# -------------------------------
# 1️⃣ Define Agents
# -------------------------------

# llm_config = OpenAI(
#     model="gpt-4o-mini",
#     temperature=0.2,
#     max_tokens=50,
#     request_timeout=30
# )
import pandas as pd

@tool("menu_reader")
def menu_reader():
    """Read an Excel file and return its contents as a list of dictionaries."""
    df = pd.read_excel('./data/food_menu.xlsx')
    return df.to_dict(orient='records')

reader_agent = Agent(
    role="Menu Reader",
    goal="Read Excel files and extract structured data from them using menu_reader tool.",
    backstory="An AI that reads tabular data and formats it for analysis.",
    tools=[menu_reader],
    verbose=True
)



order_parser_agent = Agent(
    role="Order Parser",
    goal="Understand user order input and extract item names and quantities.",
    backstory="An assistant that interprets user order text and outputs structured data.",
    tools=[],
    verbose=True
)

@tool("order_availability_checker")
def order_availability_checker(order_data: list, menu_data: list):
    """
    Checks if ordered items are available in the menu.
    Returns available items with price and total bill.
    """
    available_items = []
    total_bill = 0

    for order in order_data:
        item_name = order["item"].strip().lower()
        quantity = order.get("quantity", 1)

        match = next((m for m in menu_data if m["item"].strip().lower() == item_name), None)
        if match and str(match.get("availability", "")).lower() == "yes":
            item_total = match["price"] * quantity
            available_items.append({
                "item": match["item"],
                "quantity": quantity,
                "price": match["price"],
                "item_total": item_total
            })
            total_bill += item_total

    return {
        "available_items": available_items,
        "total_bill": total_bill
    }

billing_agent = Agent(
    role="Order Validator",
    goal="Check ordered items against menu and compute total bill.",
    backstory="An assistant that validates availability and calculates billing.",
    tools=[order_availability_checker],
    verbose=True
)

# -------------------------------
# 2️⃣ Define Tasks
# -------------------------------
# --- TASK 1: Read Menu ---
task1 = Task(
    description=(
        "Read the Excel file at './data/food_menu.xlsx' and use the 'menu_reader' tool "
        "to convert it into a list of dictionaries, each containing item, price, and availability."
    ),
    agent=reader_agent,
    expected_output="A list of dictionaries, e.g. [{'item': 'Pizza', 'price': 250, 'availability': 'Yes'}, ...]",
    output_key="menu_data"
)


# --- TASK 2: Parse User Order ---
user_order = "I would like to order 2 French Fries and 1 Chocolate Shake"
task2 = Task(
    description=(
        f"Parse the user's order: {user_order} "
        "Extract item names and quantities and return a list of dicts like "
        "[{'item': 'Pizza', 'quantity': 2}]."
    ),
    agent=order_parser_agent,
    expected_output="List of dictionaries with 'item' and 'quantity' keys.",
    inputs={f"user_input": {user_order}}, # ✅ static input here
    output_key = "order_data"
)


task3 = Task(
    description=(
        "Check if each ordered item in 'order_data' is available in 'menu_data'. "
        "Return a list of available items (with name, quantity, price, and item_total) "
        "and the total bill amount."
    ),
    agent=billing_agent,
    expected_output="Dictionary with keys: available_items and total_bill.",
    context=[task1, task2],
    output_key="final_result"
)


# -------------------------------
# 3️⃣ Define and Run Crew
# -------------------------------

crew = Crew(
    agents=[reader_agent, order_parser_agent, billing_agent],
    tasks=[task1, task2, task3]
    # process = Process.sequential,
    # planning=True,
    # memory=True
    # # verbose=True
)

result = crew.kickoff()
print("\n✅ Final Result:", result)

