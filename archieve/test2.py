from dotenv import load_dotenv
load_dotenv()
import os
from crewai import Agent, Task, Crew
import random


calc_agent = Agent(
    role="Calculator",
    goal="Generate random lists of numbers using reasoning.",
    backstory="An AI agent that simulates random number generation.",
    tools=[]  # no tools — uses reasoning to simulate output
)

task1 = Task(
    description="Generate a list of five random numbers between 51 and 70.",
    agent=calc_agent,
    expected_output="A Python list of integers between 51 and 70.",
    output_key="numbers"
)

crew1 = Crew(
    agents=[calc_agent],
    tasks=[task1]
)

result = crew1.kickoff()
print("\n✅ Crew 1 Result:", result)




