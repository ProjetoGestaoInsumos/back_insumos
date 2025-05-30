from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base
import enum

class MovementType(str, enum.Enum):
    in_ = "in"
    out = "out"

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    pop_id = Column(Integer, ForeignKey("pops.id"), nullable=True)

    stock = relationship("Stock", back_populates="movements")
    user = relationship("User")
    pop = relationship("Pop", back_populates="movements")
