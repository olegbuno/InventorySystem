from fastapi import FastAPI

from app import auth
from app.routers import items

app = FastAPI()

# Include routers
app.include_router(items.router)
app.include_router(auth.router, tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Cyberpunk Inventory Management System"}
