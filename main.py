from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    environment = os.getenv("APP_ENV", "development")
    return {"message": "Hello from Kubernetes!", "environment": environment}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


    