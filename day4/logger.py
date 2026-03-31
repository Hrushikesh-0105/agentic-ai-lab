import json
from datetime import datetime

LOG_FILE = "agent_logs.json"


def log_interaction(user_input, selected_tool, tool_input, output):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "selected_tool": selected_tool,
        "tool_input": tool_input,
        "output": output
    }

    try:
        # Append to file
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print("Logging error:", e)