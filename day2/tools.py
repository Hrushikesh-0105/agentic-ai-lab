import requests
import re
import os
import geocoder
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# CONFIGURATION
# ---------------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")

genai.configure(api_key=LLM_API_KEY)

# Initialize the model once globally for better performance
# Using gemini-1.5-flash or gemini-3-flash
summarizer_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction="You are a concise summarizer."
)

# ---------------------------
# TOOL 1: CALCULATOR
# ---------------------------
def calculator_tool(expression: str):
    try:
        # Whitelist check for safety
        if not re.match(r'^[0-9+\-*/(). ]+$', expression):
            return "Invalid expression! Only numbers and basic operators are allowed."
        
        # eval is powerful but risky; the regex above makes it "safe enough" for hobby use
        result = eval(expression)
        return f"Result: {result}"
    except Exception:
        return "Error in calculation. Check your syntax."

# ---------------------------
# HELPER: GET CURRENT LOCATION
# ---------------------------
def get_current_city():
    try:
        g = geocoder.ip('me')
        if g.city:
            return g.city.lower()
    except Exception:
        pass
    return "hyderabad"  # Consistent fallback

# ---------------------------
# TOOL 2: WEATHER
# ---------------------------
def weather_tool(city: str = None):
    if not city:
        city = get_current_city()
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5) # Added timeout for safety
        data = response.json()
        
        if data.get("cod") != 200:
            return f"Error: {data.get('message', 'City not found')}"
        
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city.title()}: {temp}°C, {desc}"
    except Exception:
        return "Error fetching weather data."

# ---------------------------
# TOOL 3: SUMMARIZER
# ---------------------------
def summarizer_tool(text: str):
    if len(text.strip()) < 20:
        return "Text too short to summarize."

    try:
        # Re-using the globally defined model
        response = summarizer_model.generate_content(
            f"Summarize this text:\n{text}",
            generation_config=genai.types.GenerationConfig(temperature=0.3)
        )
        return response.text
    except Exception as e:
        return f"Error in summarization: {str(e)}"

# ---------------------------
# TOOL REGISTRY
# ---------------------------
TOOLS = {
    "calculator": calculator_tool,
    "weather": weather_tool,
    "summarizer": summarizer_tool
}