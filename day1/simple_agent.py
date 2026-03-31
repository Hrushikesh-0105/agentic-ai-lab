import datetime
import re

# ---------------------------
# 1. INPUT HANDLER
# ---------------------------
def get_user_input():
    user_input = input("Enter your command: ")
    return user_input.strip().lower()


# ---------------------------
# 2. DECISION LOGIC
# ---------------------------
def detect_intent(user_input):
    if "hello" in user_input or "hi" in user_input:
        return "greeting"
    
    elif "date" in user_input:
        return "date"
    
    elif "calculate" in user_input:
        return "calculation"
    
    else:
        return "unknown"


# ---------------------------
# 3. ACTION EXECUTION
# ---------------------------
def execute_action(intent, user_input):
    
    if intent == "greeting":
        return "Hello! How can I help you?"
    
    elif intent == "date":
        return f"Today's date is {datetime.date.today()}"
    
    elif intent == "calculation":
        return handle_calculation(user_input)
    
    else:
        return "Sorry, I didn't understand that."


# ---------------------------
# HELPER FUNCTION (TOOL)
# ---------------------------
def handle_calculation(user_input):
    try:
        # Extract expression after 'calculate'
        expression = user_input.replace("calculate", "").strip()
        
        # Basic safety check (only numbers + operators)
        if not re.match(r'^[0-9+\-*/(). ]+$', expression):
            return "Invalid expression!"
        
        result = eval(expression)
        return f"Result: {result}"
    
    except Exception:
        return "Error in calculation."


# ---------------------------
# MAIN AGENT LOOP
# ---------------------------
def run_agent():
    print("Simple AI Agent (type 'exit' to quit)")
    
    while True:
        user_input = get_user_input()
        
        if user_input == "exit":
            print("Goodbye!")
            break
        
        intent = detect_intent(user_input)
        response = execute_action(intent, user_input)
        
        print(response)


# Run the agent
if __name__ == "__main__":
    run_agent()