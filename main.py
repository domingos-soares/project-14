"""Standalone healthcheck script.

This file contains the healthcheck functionality extracted from app/main.py
for easy access and testing.
"""

from datetime import datetime
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import check_db_health


async def healthcheck():
    """Perform a comprehensive healthcheck.
    
    Returns:
        dict: Healthcheck status including database connectivity
    """
    # Check database health
    db_health = await check_db_health()
    overall_status = "healthy" if db_health["status"] == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "service": "Person REST API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_health
    }


async def main():
    """Run healthcheck and print results."""
    print("Running healthcheck...")
    print("-" * 50)
    
    result = await healthcheck()
    
    print(f"Status: {result["status"].upper()}")
    print(f"Service: {result["service"]}")
    print(f"Version: {result["version"]}")
    print(f"Timestamp: {result["timestamp"]}")
    print(f"\nDatabase Status: {result["database"]["status"]}")
    print(f"Database Connection: {result["database"]["database"]}")
    
    if result["database"].get("error"):
        print(f"Error: {result["database"]["error"]}")
    
    print("-" * 50)
    
    # Exit with appropriate code
    if result["status"] == "healthy":
        print("✓ All systems healthy")
        sys.exit(0)
    else:
        print("✗ System unhealthy")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
