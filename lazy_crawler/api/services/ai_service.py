import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Model
# Using 'gemini-pro' for text and code generation
model = genai.GenerativeModel("gemini-pro")


async def chat_with_data(message: str, context: str = "") -> str:
    """
    Chat with the AI about the provided data context.
    """
    if not GEMINI_API_KEY:
        return "AI Service is not configured (Missing API Key)."

    prompt = f"""
    You are a helpful data analyst assistant.
    User Question: {message}

    Context Data (Snippet):
    {context}

    Answer the user's question based on the context. If the answer is not in the context, say so, but try to be helpful.
    Keep the answer concise and professional.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"


async def generate_chart_config(description: str, data_summary: str = "") -> dict:
    """
    Generate a Chart.js configuration based on the description and data summary.
    """
    if not GEMINI_API_KEY:
        return {"error": "AI Service not configured"}

    prompt = f"""
    You are a data visualization expert.
    User Request: {description}

    Data Summary:
    {data_summary}

    Generate a JSON object representing a Chart.js (version 3/4) configuration.
    The output must be VALID JSON ONLY. Do not include markdown formatting (```json ... ```).
    Structure:
    {{
        "type": "bar", // or line, pie, etc.
        "data": {{
            "labels": [...],
            "datasets": [{{
                "label": "...",
                "data": [...],
                "backgroundColor": "..."
            }}]
        }},
        "options": {{ ... }}
    }}

    Make the charts look modern and professional.
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        config = json.loads(text)
        return config
    except Exception as e:
        return {"error": f"Failed to generate chart: {str(e)}"}
