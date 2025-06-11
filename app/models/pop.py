from sqlalchemy import Column, Integer, ForeignKey, String, JSON, Date, Enum as SQLAEnum
from app.database.db import Base
import enum

class TurnoEnum(enum.Enum):
    manha = "manha"
    tarde = "tarde"
    noite = "noite"

class StatusEnum(enum.Enum):
    pendente = "pendente"
    aprovado = "aprovado"
    cancelado = "cancelado"

class POP(Base):
    __tablename__ = "pop"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)
    docente_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    curso = Column(String, nullable=False)
    disciplina = Column(String, nullable=False)
    protocolo = Column(String, nullable=False)
    turno = Column(SQLAEnum(TurnoEnum), nullable=False)
    date = Column(Date, nullable=False)
    n_students = Column(Integer, nullable=False)
    n_groups = Column(Integer, nullable=False)
    extra_items = Column(JSON, nullable=True)
    objective = Column(String, nullable=True)
    status = Column(SQLAEnum(StatusEnum), default=StatusEnum.pendente, nullable=False)