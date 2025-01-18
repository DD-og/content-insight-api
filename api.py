from fastapi import FastAPI, HTTPException
from content_generator import validate_input, generate_article, SCHEMA
from typing import Dict, Any
from jsonschema import ValidationError
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Content Generator API",
    description="API for generating content based on brand information",
    version="1.0.0"
)

@app.post("/generate")
async def generate_content(data: Dict[str, Any]):
    try:
        # Validate input
        validate_input(data)
        
        # Generate article
        result = generate_article(data)
        return {"content": result}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schema")
async def get_schema():
    return SCHEMA

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("api:app", host="0.0.0.0", port=args.port, reload=True)
