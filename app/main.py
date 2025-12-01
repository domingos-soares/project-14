"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.person import router as person_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.description,
        debug=settings.debug
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
                "GET /persons": "Get all persons",
                "GET /persons/{id}": "Get a specific person",
                "POST /persons": "Create a new person",
                "PUT /persons/{id}": "Update a person",
                "DELETE /persons/{id}": "Delete a person"
            },
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    return app


app = create_app()
