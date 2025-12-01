"""Main FastAPI application."""

from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.person import router as person_router
from app.db import init_db, check_db_health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events.
    
    Handles startup and shutdown events.
    """
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Cleanup if needed


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.description,
        debug=settings.debug,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(person_router)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Welcome endpoint with API information."""
        return {
            "message": f"Welcome to the {settings.app_name}",
            "version": settings.app_version,
            "endpoints": {
                "GET /health": "Healthcheck endpoint",
                "GET /persons": "Get all persons",
                "GET /persons/{id}": "Get a specific person",
                "POST /persons": "Create a new person",
                "PUT /persons/{id}": "Update a person",
                "DELETE /persons/{id}": "Delete a person"
            },
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    # Healthcheck endpoint
    @app.get("/health", tags=["Health"])
    async def healthcheck():
        """Healthcheck endpoint for monitoring and load balancers.
        
        Returns service status including database connectivity.
        """
        db_health = await check_db_health()
        overall_status = "healthy" if db_health["status"] == "healthy" else "unhealthy"
        
        return {
            "status": overall_status,
            "service": settings.app_name,
            "version": settings.app_version,
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_health
        }
    
    return app


app = create_app()
