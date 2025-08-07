from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get API key from environment
api_key = os.getenv("LANGFLOW_API_KEY")
if not api_key:
    raise ValueError("LANGFLOW_API_KEY not set in environment variables.")

# Langflow public or local endpoint
LANGFLOW_URL = "http://localhost:7860/api/v1/run/cfe1ef2e-25c1-4225-8099-2ea71d418721"

# Input data structure
class InputPrompt(BaseModel):
    message: str

@app.post("/run")
def run_langflow(prompt: InputPrompt):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": prompt.message
    }

    try:
        response = requests.post(LANGFLOW_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
