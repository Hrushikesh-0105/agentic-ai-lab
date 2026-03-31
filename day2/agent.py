from tools import TOOLS

# ---------------------------
# INPUT HANDLER
# ---------------------------
def get_user_input():
    return input("\nEnter command: ").strip().lower()


# ---------------------------
# INTENT DETECTION
# ---------------------------
def detect_intent(user_input):
    
    if "calculate" in user_input:
        return "calculator"
    
    elif "weather" in user_input:
        return "weather"
    
    elif "summarize" in user_input:
        return "summarizer"
    
    else:
        return "unknown"


# ---------------------------
# PARAM EXTRACTION
# ---------------------------
def extract_parameters(intent, user_input):
    
    if intent == "calculator":
        return user_input.replace("calculate", "").strip()
    
    elif intent == "weather":
        words = user_input.split()
        if "in" in words:
            return words[-1]
        return None  # triggers current location
    
    elif intent == "summarizer":
        return user_input.replace("summarize", "").strip()
    
    return None


# ---------------------------
# AGENT LOOP
# ---------------------------
def run_agent():
    print("Tool-Using Agent (type 'exit' to quit)")
    
    while True:
        user_input = get_user_input()
        
        if user_input == "exit":
            print("Goodbye!")
            break
        
        intent = detect_intent(user_input)
        
        if intent == "unknown":
            print("I don't understand.")
            continue
        
        params = extract_parameters(intent, user_input)
        
        print(f"Detected intent: {intent}")
        print(f"Using tool: {intent}")
        
        tool_function = TOOLS[intent]
        result = tool_function(params)
        
        print(f"Result: {result}")


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    run_agent()


    