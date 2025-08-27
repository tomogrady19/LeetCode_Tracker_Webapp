from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers import frontend, api

app = FastAPI()

# Init app, serve frontend files and include API routes
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(frontend.router)
app.include_router(api.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    """Run the following in the terminal, then go to the following link"""
    # uvicorn main:app --reload
    # http://localhost:8000/
