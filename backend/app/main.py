"""
AI Business Portfolio Manager - FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.core.database import engine, init_db
from app.modules.trends import router as trends_router
from app.modules.ideas import router as ideas_router
from app.modules.agents import router as agents_router

# Initialize structured logging
logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="AI Business Portfolio Manager",
    description="Automated business management system using AI agents",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT
    }


# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API root endpoint
    """
    return {
        "message": "AI Business Portfolio Manager API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include Module Routers
app.include_router(
    trends_router.router,
    prefix="/api/v1/trends",
    tags=["Trends"]
)

app.include_router(
    ideas_router.router,
    prefix="/api/v1/ideas",
    tags=["Ideas"]
)

app.include_router(
    agents_router.router,
    prefix="/api/v1/agents",
    tags=["Agents"]
)


# Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    """
    logger.error("Unhandled exception", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc) if settings.DEBUG else "Internal server error"
            }
        }
    )


# Startup Event
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    """
    logger.info("Starting AI Business Portfolio Manager API", version="0.1.0")

    # Database initialization
    init_db()
    logger.info("Database tables initialized")


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    """
    logger.info("Shutting down AI Business Portfolio Manager API")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
