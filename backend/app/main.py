"""
Main application file for Julius.
This file contains the FastAPI application instance and basic configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user_router, category_router, expense_router, category_budget_router, transaction_router, auth_router, dashboard_router

app: FastAPI = FastAPI(
    title="Julius",
    description="API for tracking monthly expenses",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:5173", # Alternative localhost
        "http://127.0.0.1:3000", # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(expense_router, prefix="/api/v1")
app.include_router(category_budget_router, prefix="/api/v1")
app.include_router(transaction_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Julius API is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}