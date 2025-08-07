from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Input schema
class PromptInput(BaseModel):
    message: str

# Load API key from environment variable
try:
    api_key = os.environ["sk-s7MVeXQ4hXxG4kSkrV72eQgjIQXc8KSAPgcYBWn6DWg"]
except KeyError:
    raise ValueError("LANGFLOW_API_KEY not set")

# Langflow endpoint (running on same Render instance or another host)
LANGFLOW_URL = "http://localhost:7860/api/v1/run/cfe1ef2e-25c1-4225-8099-2ea71d418721"

@app.post("/run")
def run_langflow(input: PromptInput):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": input.message
    }

    try:
        response = requests.post(LANGFLOW_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
