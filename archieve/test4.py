from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv("OPENAI_API_KEY"))
from langchain_openai import OpenAI
from crewai import Agent, Task, Crew
from crewai.tools import tool
import random




order_parser_agent = Agent(
    role="Order Parser",
    goal="Understand user order input and extract item names and quantities.",
    backstory="An assistant that interprets user order text and outputs structured data.",
    tools=[],
    verbose=True
)


# --- TASK 2: Parse User Order ---
user_order = "I want 2 cold coffee and may be sandwich 1 "
task2 = Task(
    description=(
        f"Parse the user's order: {user_order} "
        "Extract item names and quantities and return a list of dicts like "
        "[{'item': 'Pizza', 'quantity': 2}]."
    ),
    agent=order_parser_agent,
    expected_output="List of dictionaries with 'item' and 'quantity' keys.",
    inputs={f"user_input": {user_order}} # ✅ static input here
)


crew = Crew(
    agents=[order_parser_agent],
    tasks=[task2]
)

result = crew.kickoff()
print("\n✅ Final Result:", result)


# Prompts 
# "I want 2 cold coffee and may be sandwich 1 "
# "I want 1 veg burger coffee and 2 pizza "


