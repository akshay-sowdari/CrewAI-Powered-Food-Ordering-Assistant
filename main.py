from dotenv import load_dotenv
load_dotenv()
import os
# print(os.getenv("OPENAI_API_KEY"))
from langchain_openai import OpenAI
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import streamlit as st
import pandas as pd


# llm_config = OpenAI(
#     model="gpt-4o-mini",
#     temperature=0.2,
#     max_tokens=50,
#     request_timeout=30
# )


# Menu Reader Agent

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


# Order Parser Agent
order_parser_agent = Agent(
    role="Order Parser",
    goal="Understand user order input and extract item names and quantities.",
    backstory="An assistant that interprets user order text and outputs structured data.",
    tools=[],
    verbose=True
)

# Availability Checker Agent
@tool("order_availability_checker")
def order_availability_checker(order_data: list, menu_data: list):
    """
    Checks if ordered items are available in the menu.
    Returns a human-readable message about available/unavailable items and total bill.
    """
    available_items = []
    unavailable_items = []
    total_bill = 0

    for order in order_data:
        item_name = order["item"].strip().lower()
        quantity = order.get("quantity", 1)

        # Match against menu
        match = next((m for m in menu_data if m["item"].strip().lower() == item_name), None)

        if match:
            if str(match.get("availability", "")).lower() == "yes":
                item_total = match["price"] * quantity
                available_items.append({
                    "item": match["item"],
                    "quantity": quantity,
                    "price": match["price"],
                    "item_total": item_total
                })
                total_bill += item_total
            else:
                unavailable_items.append(match["item"])
        else:
            unavailable_items.append(order["item"])

    # Constructing the response message
    if not available_items and unavailable_items:
        return f"Hello Sir! Unfortunately, none of your ordered items ({', '.join(unavailable_items)}) are available right now. Please try ordering something else from our menu."

    elif available_items and unavailable_items:
        available_str = ", ".join([f"{i['item']} costing ${i['price']} per unit" for i in available_items])
        details = ", ".join([f"{i['quantity']} - {i['item']}" for i in available_items])
        return (
            f"Hello Sir! Thanks for your order. Unfortunately, we dont have {', '.join(unavailable_items)} available. "
            f"But we do have {available_str}. For the ordered quantities ({details}), "
            f"your total bill will be ${total_bill}."
        )

    elif available_items and not unavailable_items:
        available_str = ", ".join([f"{i['item']} costing ${i['price']} per unit" for i in available_items])
        details = ", ".join([f"{i['quantity']} - {i['item']}" for i in available_items])
        return (
            f"Hello Sir! Thanks for your order. All items are available — {available_str}. "
            f"For your quantities ({details}), your total bill is ${total_bill}."
        )

    else:
        return "Sorry, I couldnt match any items from your order with the menu."



billing_agent = Agent(
    role="Order Validator",
    goal="Check ordered items against menu and compute total bill.",
    backstory="An assistant that validates availability and calculates billing.",
    tools=[order_availability_checker],
    verbose=True
)


# Streamlit UI and Task Definitions
st.title("🍽️ AI Food Ordering Assistant")

user_order = st.text_input("Enter your order:", placeholder="e.g. I'd like to order 2 burgers and 1 coke")

if st.button("Submit Order",type="primary"):
    if not user_order.strip():
        st.warning("Please enter your order first.")
    else:
        task1 = Task(
            description=(
            "Read the Excel file at './data/food_menu.xlsx' and use the 'menu_reader' tool "
            "to convert it into a list of dictionaries, each containing item, price, and availability."
            ),
            agent=reader_agent,
            expected_output="A list of dictionaries, e.g. [{'item': 'Pizza', 'price': 250, 'availability': 'Yes'}, ...]",
            output_key="menu_data"
        )

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
            "Using 'order_data' and 'menu_data', check item availability and billing using the 'order_availability_checker' tool. "
            "Return a polite, conversational response summarizing which items are available or unavailable, "
            "their prices, and the total bill amount. Format the response naturally as if a waiter is speaking."
            ),
            agent=billing_agent,
            expected_output=(
                "A natural language message using the 'order_availability_checker' tool return statements. \n"
                ),
            context=[task1, task2],
            output_key="final_result"
            # human_input=True
        )

        # Crew Definition
        crew = Crew(
            agents=[reader_agent, order_parser_agent, billing_agent],
            tasks=[task1, task2, task3],
            process = Process.sequential
            # planning=True,
            # memory=True,
            # verbose=True
        )

        result = crew.kickoff()
        st.success(" Final Result:")
        st.write(result.raw)












