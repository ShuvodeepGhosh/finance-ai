from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

print("Configuring Gemini API key...")
api_key = os.getenv("GEMINI_API_KEY")
print("Gemini API Key:", api_key)
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def build_prompt(metrics, categories):

    prompt = f"""
You are a financial advisor.

The currency of the user's transactions is in Indian Rupees (₹).
User Financial Data:

Income: {metrics['income']}
Expenses: {metrics['expenses']}
Net Savings: {metrics['net_savings']}
Savings Rate: {metrics['savings_rate']}

Category Spending:
{categories}

Provide 3 short financial insights and suggestions.
Keep advice practical.
"""

    return prompt

def generate_ai_advice(metrics, categories):

    prompt = build_prompt(metrics, categories)

    response = model.generate_content(prompt)

    return response.text