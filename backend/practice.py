# 1. The Pydantic Model Challenge
# Scenario: You are building an endpoint for a GenAI feature where a user submits a prompt and a "creativity" score (temperature).
# Question: How would you define a Pydantic schema to ensure the prompt is not empty and the temperature is a float between 0.0 and 1.0? Write a basic FastAPI POST endpoint using this model.

# What they are looking for:

# Correct use of BaseModel.

# Validation using Field or Annotated (e.g., ge=0, le=1).

# Proper status code usage (FastAPI returns 422 automatically if validation fails).

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, Field

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The prompt for content generation. Must not be empty.")
    temperature: float = Field(..., ge=0.0, le=1.0, description="The creativity score (temperature) for generation. Must be between 0.0 and 1.0.")

@router.post("/generate")
async def generate_content(request: GenerateRequest):
    return {"message": "Content generated successfully!", "prompt": request.prompt, "temperature": request.temperature}