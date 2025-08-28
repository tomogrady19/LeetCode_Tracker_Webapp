from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers import frontend, api
from database import create_tables
import os

app = FastAPI()


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    await create_tables()

# Init app, serve frontend files and include API routes
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(frontend.router)
app.include_router(api.router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

    """Run the following in the terminal, then go to the following link"""
    # uvicorn main:app --reload
    # http://localhost:8000/
