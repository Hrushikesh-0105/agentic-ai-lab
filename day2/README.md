# Assignment 2: Tool-Using Agent

## Objective
Enable the agent to use external tools.

## Approach
- Tools are defined in tools.py
- Agent selects tool based on input
- Tools include:
  - Calculator
  - Weather API
  - Text summarizer (LLM)

## Installation
pip install requests python-dotenv geocoder

## Environment Variables
Create .env file:
OPENWEATHER_API_KEY=your_key
LLM_API_KEY=your_key

## Execution
python agent.py

## Learning Outcomes
- Tool abstraction
- API integration
- Modular programming
