# main.py — FastAPI application entry point
# Phase 1: Basic setup — just getting the server running

from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Automated Regulatory Compliance Mapping System",
    description="Maps ISO 27001 controls to NIST CSF using NLP",
    version=os.getenv("VERSION", "1.0.0"),
)

# Root endpoint — just to test if server is running
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
        "phase": "Phase 1 — Backend Foundation"
    }

# Health check endpoint
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": os.getenv("VERSION", "1.0.0")
    }
