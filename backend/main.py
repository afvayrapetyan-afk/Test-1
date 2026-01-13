"""
AI Business Portfolio Manager - Backend API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Business Portfolio Manager API",
    description="Backend API for managing AI agents and code integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # Vite (current port)
        "http://localhost:5173",  # Vite (default)
        "http://localhost:3000",  # React
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from api import code, agents, github_webhooks

# Register routers
app.include_router(code.router, prefix="/api", tags=["code"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(github_webhooks.router, prefix="/webhooks", tags=["webhooks"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "AI Business Portfolio Manager API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "github_configured": bool(os.getenv("GITHUB_TOKEN")),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY"))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True"
    )
