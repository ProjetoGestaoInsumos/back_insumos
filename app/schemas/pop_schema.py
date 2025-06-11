from pydantic import BaseModel
from datetime import date
from typing import Dict, Optional, List, Literal


class ExtraItem(BaseModel):
    item_id: int
    quantity: float  # ou str se quiser manter a unidade (ex: "300 ml")

class POPCreate(BaseModel):
    recipe_id: int
    docente_id: int
    curso: str
    disciplina: str
    protocolo: str
    turno: Literal["manha", "tarde", "noite"]
    date: date
    n_students: int
    n_groups: int
    objective: Optional[str]
    extra_items: Optional[List[ExtraItem]] = []


class POPStatusUpdate(BaseModel):
    status: Literal["pendente", "aprovado", "cancelado"]


class POPResponse(BaseModel):
    id: int
    recipe_id: int
    docente_id: int
    docente_nome: str
    recipe_name: str
    curso: str
    disciplina: str
    protocolo: str
    turno: str
    date: date
    n_students: int
    n_groups: int
    objective: Optional[str]
    extra_items: Optional[List[ExtraItem]]
    status: str

    class Config:
        from_attributes = True


# class POPCheckRequest(BaseModel):
#     recipe_id: int
#     requested_quantity: Optional[int] = 1  # optional, default is 1

#     class Config:
#         orm_mode = True


#class POPCheckResponse(BaseModel):
#    available: Dict[str, int]
#    missing: Dict[str, int]
#    status: str

#    class Config:
#        orm_mode = True