from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  
from app.database.db import get_db

router = APIRouter()

@router.get("/test-conn/")
def test_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "ok", "result": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
