# Assignment 3: LLM-Based Agent

## Objective
Use an LLM to decide which tool to call.

## Approach
- Gemini LLM selects tool
- Returns structured JSON
- Agent executes tool
- Logs interactions

## Installation
pip install google-generativeai python-dotenv

## Environment Variables
LLM_API_KEY=your_gemini_api_key

## Execution
python agent.py

## Logging
Logs stored in agent_logs.json

## Learning Outcomes
- Prompt-based reasoning
- LLM integration
- Tool selection via AI
