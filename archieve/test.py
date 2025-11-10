from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv("OPENAI_API_KEY"))
from langchain_openai import OpenAI
from crewai import Agent, Task, Crew
from crewai.tools import tool
import random

import openai
openai.log = "info"

# -------------------------------
# 1️⃣ Define Agents
# -------------------------------

# llm_config = OpenAI(
#     model="gpt-4o-mini",
#     temperature=0.2,
#     max_tokens=50,
#     request_timeout=30
# )


@tool("random_number_generator")
def random_number_generator(start: int, end: int, count: int):
    """Generate a list of random numbers within a specified range."""
    return [random.randint(start, end) for _ in range(count)]


calc_agent = Agent(
    role="Calculator",
    goal="Generate random lists of numbers using tools.",
    backstory="An AI agent that uses a random number generation tool.",
    tools=[random_number_generator],
    # llm=llm_config,
    verbose=True
)

sum_agent = Agent(
    role="Summer",
    goal="Compute the sum of lists using a calculation tool.",
    backstory="An AI agent that calculates totals using Python tools.",
    tools=[],
    # llm=llm_config,
    verbose=True
)       

# -------------------------------
# 2️⃣ Define Tasks
# -------------------------------

task1 = Task(
    description="Generate a list of 2 random numbers between 6 and 15 using the random_number_generator tool.",
    agent=calc_agent,
    expected_output="A Python list of integers between 6 and 15.",
    output_key="numbers"
)


task2 = Task(
    description="Take the list of numbers from the previous task and calculate their sum and avergae.",
    agent=sum_agent,
    expected_output="The sum and average of the list of numbers as an integer.",
    input_keys=["numbers"],
    human_input=True
)

# -------------------------------
# 3️⃣ Define and Run Crew
# -------------------------------

crew = Crew(
    agents=[calc_agent, sum_agent],
    tasks=[task1, task2]
)

result = crew.kickoff()
print("\n✅ Final Result:", result)



