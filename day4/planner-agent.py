import os
import json
import re
import google.generativeai as genai

from tools import TOOLS
from logger import log_interaction

# ---------------------------
# GEMINI SETUP
# ---------------------------
LLM_API_KEY = os.getenv("LLM_API_KEY")
genai.configure(api_key=LLM_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------
# SAFE JSON PARSER
# ---------------------------
def safe_parse_json(text):
    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("JSON parse error:", e)
    return None


# ---------------------------
# PLAN GENERATION
# ---------------------------
def create_plan(user_input):
    prompt = f"""
You are an AI planning agent.

Break the task into steps using tools.

Available tools:
- calculator → math operations
- weather → get temperature of a city
- summarizer → summarize final result

IMPORTANT RULES:
1. Use {{result1}}, {{result2}} etc. for previous outputs
2. If calculating averages, extract numeric values from weather
3. DO NOT summarize vague text
4. Return ONLY VALID JSON
5. NO explanation, NO markdown

FORMAT:
[
  {{
    "step": 1,
    "tool": "tool_name",
    "input": "input"
  }}
]

EXAMPLES:

User: Find average of 5, 10, 15 and summarize
[
  {{"step": 1, "tool": "calculator", "input": "(5+10+15)/3"}},
  {{"step": 2, "tool": "summarizer", "input": "The result is {{result1}}"}}
]

User: Average temperature of mumbai and hyderabad
[
  {{"step": 1, "tool": "weather", "input": "mumbai"}},
  {{"step": 2, "tool": "weather", "input": "hyderabad"}},
  {{"step": 3, "tool": "calculator", "input": "({{result1}}+{{result2}})/2"}}
]

Now:
User: {user_input}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    plan = safe_parse_json(text)

    if not plan:
        print("Raw LLM output:")
        print(text)

    return plan


# ---------------------------
# EXTRACT TEMPERATURE
# ---------------------------
def extract_temperature(output):
    match = re.search(r"([-+]?\d*\.\d+|\d+)", output)
    return float(match.group()) if match else None


# ---------------------------
# EXECUTION ENGINE
# ---------------------------
def execute_plan(plan):
    results = []

    for step in plan:
        tool = step["tool"]
        tool_input = step["input"]

        # Replace placeholders
        for i, res in enumerate(results):
            tool_input = tool_input.replace(f"{{result{i+1}}}", str(res))

        print(f"\nStep {step['step']}: {tool}")
        print(f"Input: {tool_input}")

        if tool not in TOOLS:
            print("Invalid tool:", tool)
            return None

        output = TOOLS[tool](tool_input)

        print(f"Output: {output}")

        # Store processed result
        if tool == "weather":
            temp = extract_temperature(output)
            results.append(temp)
        else:
            results.append(output)

    return results[-1]


# ---------------------------
# MAIN LOOP
# ---------------------------
def run_agent():
    print("Planning Agent (type 'exit' to quit)")
    
    while True:
        user_input = input("\nEnter command: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # ---------------------------
        # PLAN
        # ---------------------------
        print("\nGenerating plan...")
        plan = create_plan(user_input)
        
        if not plan:
            print("Could not generate plan.")
            continue
        
        print("\nPlan:")
        for step in plan:
            print(step)
        
        # ---------------------------
        # EXECUTE
        # ---------------------------
        print("\nExecuting plan...")
        final_result = execute_plan(plan)
        
        print("\nFinal Result:", final_result)
        
        # ---------------------------
        # LOGGING
        # ---------------------------
        log_interaction(
            user_input=user_input,
            selected_tool="planner",
            tool_input=str(plan),
            output=final_result
        )


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    run_agent()