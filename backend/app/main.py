from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routes import router

app = FastAPI(title="Pet Rescue Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directory exists
os.makedirs("app/storage/pet_images", exist_ok=True)

# Serve images statically
app.mount("/static", StaticFiles(directory="app/storage"), name="static")

app.include_router(router)
