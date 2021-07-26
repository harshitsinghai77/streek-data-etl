"""Main app which serves the application."""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import database, engine, metadata
from app.config.settings import get_setting
from app.routers.cliff import cliff_router

settings = get_setting()
metadata.create_all(engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Connect to database on startup."""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Disconnect to database on shutdown."""
    await database.disconnect()


@app.get("/")
def index():
    """Generic message if backend is deployed succesfully."""
    return "App succesfully running."


app.include_router(
    cliff_router,
    prefix="/api",
    tags=["Items"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
