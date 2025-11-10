# 🍽️ AI Food Ordering Assistant using CrewAI & Streamlit

An intelligent restaurant assistant powered by **CrewAI** that reads menus, understands user orders, checks item availability, and generates billing responses conversationally — just like a real waiter!

---

## 🚀 Overview

This project showcases a **multi-agent CrewAI system** combined with a **Streamlit UI** to automate the food ordering process.  
Users can type natural language orders (e.g., “2 pizzas and 1 coke”), and the system will:

1. Read the restaurant menu from an Excel sheet  
2. Parse and understand the user's text-based order  
3. Validate item availability  
4. Compute the final bill  
5. Respond politely with a waiter-style message  

---

## 🧠 Architecture

The system is composed of three AI Agents coordinated by **CrewAI**:

| Agent | Role | Description |
|-------|------|-------------|
| **Menu Reader Agent** | Data Extractor | Reads the Excel menu and returns structured data |
| **Order Parser Agent** | Interpreter | Parses the user’s text input into structured order data |
| **Billing Agent** | Validator | Checks availability and computes the final bill |

Each agent performs its respective **Task**, and the CrewAI **Crew** orchestrates their sequential execution.

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **CrewAI** – Multi-agent orchestration framework
- **LangChain** – LLM integration (OpenAI backend)
- **Streamlit** – Front-end user interface
- **Pandas** – Excel data handling

---

## 📁 Project Structure

project_root/
│
├── data/
│ └── food_menu.xlsx
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
└── project_description.txt