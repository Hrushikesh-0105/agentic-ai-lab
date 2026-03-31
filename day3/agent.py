import os
import json
import google.generativeai as genai
from tools import TOOLS
from logger import log_interaction # Ensure this is implemented in logger.py

# ---------------------------
# SETUP GEMINI
# ---------------------------
LLM_API_KEY = os.getenv("LLM_API_KEY")
genai.configure(api_key=LLM_API_KEY)

# Use a stable model name
# "gemini-1.5-flash" is the current standard for fast tool-use tasks
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------------
# PROMPT FOR TOOL SELECTION
# ---------------------------
def build_prompt(user_input):
    return f"""
You are an AI agent that selects the correct tool.
Available tools:
1. calculator -> for math expressions (input: the raw equation)
2. weather -> for weather queries (input: the city name)
3. summarizer -> for summarizing text (input: the full text)

Rules:
- Respond ONLY in JSON.
- If no tool matches, set "tool" to "none".

Format:
{{
  "tool": "tool_name",
  "input": "processed input for tool"
}}

Examples:

User: calculate 2 + 3
→ {{ "tool": "calculator", "input": "2 + 3" }}

User: calculate two plus three
→ {{ "tool": "calculator", "input": "2 + 3" }}

User: weather in delhi
→ {{ "tool": "weather", "input": "delhi" }}

User: weather in hyd
→ {{ "tool": "weather", "input": "hyderabad" }}

User: weather in bomba
→ {{ "tool": "weather", "input": "mumbai" }}

User: summarize AI is amazing...
→ {{ "tool": "summarizer", "input": "AI is amazing..." }}
Now process:

User: {user_input}
"""

# ---------------------------
# LLM DECISION FUNCTION
# ---------------------------
def decide_tool(user_input):
    try:
        prompt = build_prompt(user_input)
        
        # Using response_mime_type forces the model to output valid JSON
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        text = response.text.strip()
        
        # Small fix: Remove markdown code blocks if the LLM adds them despite instructions
        if text.startswith("```"):
            text = text.split("```")[1].replace("json", "").strip()

        decision = json.loads(text)
        return decision.get("tool"), decision.get("input")

    except Exception as e:
        print(f"LLM parsing error: {e}")
        return None, None

# ---------------------------
# AGENT LOOP
# ---------------------------
def run_agent():
    print("--- LLM-Based Agent Active (type 'exit' to quit) ---")
    
    while True:
        user_input = input("\nEnter command: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # 1. LLM decides tool
        tool_name, tool_input = decide_tool(user_input)
        
        # 2. Validation
        if not tool_name or tool_name == "none" or tool_name not in TOOLS:
            print(f"Agent: I'm not sure which tool to use for '{user_input}'.")
            continue
        
        print(f"-> [System] LLM Selected: {tool_name}")
        print(f"-> [System] Tool Input: {tool_input}")
        
        # 3. Execute tool
        try:
            result = TOOLS[tool_name](tool_input)
            print(f"Result: {result}")
            
            # 4. LOGGING (Optional)
            log_interaction(
                user_input=user_input,
                selected_tool=tool_name,
                tool_input=tool_input,
                output=result
            )
        except Exception as e:
            print(f"Error executing tool {tool_name}: {e}")

# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    run_agent()