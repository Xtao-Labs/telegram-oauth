import uvicorn

from src.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
        reload=settings.DEBUG,
    )
