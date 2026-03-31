# Assignment 4: Multi-Step Planning Agent

## Objective
Build an agent that solves tasks using multiple steps.

## Approach
- LLM generates a plan (list of steps)
- Each step uses a tool
- Results passed between steps
- Intermediate outputs displayed

## Architecture
Input → Plan → Execute Steps → Output

## Installation
pip install google-generativeai python-dotenv requests geocoder

## Environment Variables
LLM_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_key

## Execution
python planner_agent.py

## Example
Input: Find average of 5, 10, 15 and summarize

Steps:
1. Calculator
2. Summarizer

## Learning Outcomes
- Task decomposition
- Sequential reasoning
- Planning-based agents
