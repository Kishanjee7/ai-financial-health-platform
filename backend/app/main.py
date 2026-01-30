from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Health Assessment Platform API",
    description="API for analyzing SME financial health using AI.",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Health Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
