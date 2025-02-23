from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db

app = FastAPI(title="HR Recruitment System")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "healthy"}
