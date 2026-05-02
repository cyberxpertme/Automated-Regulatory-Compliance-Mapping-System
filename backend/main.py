# main.py
# Phase 3: Auth routes added

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models.database import engine, Base
from routes.auth import router as auth_router
import os

load_dotenv()

# Auto-create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automated Regulatory Compliance Mapping System",
    description="Maps ISO 27001 controls to NIST CSF using NLP",
    version=os.getenv("VERSION", "1.0.0"),
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "project": "Automated Regulatory Compliance Mapping System",
        "team": [
            "Md Shible Sadiqe — H-411",
            "Md Nahid Chowdhury — H-392"
        ],
        "university": "University of Dhaka — PMICS Batch 4",
        "status": "Running ✅",
        "phase": "Phase 3 — Authentication Ready"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "auth": "JWT enabled ✅"}
