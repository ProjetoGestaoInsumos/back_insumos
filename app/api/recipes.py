from fastapi import APIRouter

router = APIRouter()

# Exemplo de rota GET
@router.get("/")
def get_all():
    return {"message": "Listando recipes"}