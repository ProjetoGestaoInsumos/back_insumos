from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join("app/uploads", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return FileResponse(file_path)