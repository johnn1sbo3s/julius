"""
Main application file for Julius.
This file contains the FastAPI application instance and basic configuration.
"""

from fastapi import FastAPI
from .routes import user_router, category_router, expense_router, transaction_router

app: FastAPI = FastAPI(
    title="Julius",
    description="API for tracking monthly expenses",
    version="0.1.0"
)

# Include routers
app.include_router(user_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(expense_router, prefix="/api/v1")
app.include_router(transaction_router, prefix="/api/v1")

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Julius API is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}