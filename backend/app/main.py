"""
Main application file for Julius.
This file contains the FastAPI application instance and basic configuration.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Julius",
    description="API for tracking monthly expenses by category",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Julius API is running."}