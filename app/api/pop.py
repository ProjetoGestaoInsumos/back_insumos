import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.pop_service import generate_pop_pdf, send_pop_approval_email
from app.models.pop import POP
from app.schemas.pop_schema import POPCreate, POPResponse, POPStatusUpdate
from app.database.db import get_db
from app.models.recipe import Recipe
from app.models.user import User

router = APIRouter()

@router.post("/pop", response_model=POPResponse)
def create_pop(pop: POPCreate, db: Session = Depends(get_db)):
    pop_dict = pop.dict()
    email_destino = pop_dict.pop("email_destino")
    
    db_pop = POP(**pop_dict)
    db.add(db_pop)
    db.commit()
    db.refresh(db_pop)

    docente = db.query(User).filter(User.id == db_pop.docente_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == db_pop.recipe_id).first()
    
    pop_data = {
        **db_pop.__dict__,
        "docente_nome": docente.name if docente else "Desconhecido",
        "recipe_name": recipe.name if recipe else "Desconhecido"
    }
    
    pdf_path = generate_pop_pdf(pop_data)
    
    email_status = "E-mail enviado com sucesso!"

    try:
        send_pop_approval_email(pop_data, recipient_email=email_destino, pdf_path=pdf_path)
    except Exception as e:
        logging.error(f"Erro ao enviar o e-mail: {e}")
        email_status = f"Falha ao enviar o e-mail: {str(e)}"  # Atualiza a mensagem de erro no status do e-mail
    
    # Remove o arquivo PDF gerado após o envio ou falha
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return {**pop_data, "email_status": email_status}

@router.get("/pop", response_model=List[POPResponse])
def list_pop(db: Session = Depends(get_db)):
    pops = db.query(POP).all()
    result = []
    for pop in pops:
        docente = db.query(User).filter(User.id == pop.docente_id).first()
        recipe = db.query(Recipe).filter(Recipe.id == pop.recipe_id).first()
        result.append({
            **pop.__dict__,
            "docente_nome": docente.name if docente else "Desconhecido",
            "recipe_name": recipe.name if recipe else "Desconhecido"
        })
    return result

@router.put("/pop/{pop_id}/status")
def update_status(pop_id: int, update: POPStatusUpdate, db: Session = Depends(get_db)):
    pop = db.query(POP).filter(POP.id == pop_id).first()
    if not pop:
        raise HTTPException(status_code=404, detail="POP não encontrado")
    pop.status = update.status
    db.commit()
    return {"status": "atualizado"}