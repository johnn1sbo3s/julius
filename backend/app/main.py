"""
Main application file for Julius.
This file contains the FastAPI application instance and basic configuration.
"""

from fastapi import FastAPI
from app.routes.transactions import transactions_router

app: FastAPI = FastAPI(
    title="Julius",
    description="API for tracking monthly expenses",
    version="0.1.0"
)

app.include_router(transactions_router)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Julius API is running."}