from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.image import Image
import os

router = APIRouter()
UPLOAD_DIR = "app/uploads"

@router.post("/upload-image/")
async def upload_image(image: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed_types = ["image/jpeg", "image/png"]
    max_size = 5 * 1024 * 1024  # 5 MB

    # Lê o conteúdo da imagem
    content = await image.read()

    # Valida o tipo
    if image.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido")

    # Valida o tamanho
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="Arquivo excede o tamanho máximo permitido")

    # Salva o arquivo no disco
    file_location = os.path.join(UPLOAD_DIR, image.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(content)

    # Salva os metadados no banco
    image_record = Image(
        filename=image.filename,
        filepath=file_location,
        content_type=image.content_type
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    return {"message": "Imagem salva com sucesso", "id": image_record.id}