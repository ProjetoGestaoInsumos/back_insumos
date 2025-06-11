from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
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
    quantity = Column(Float, nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
   

    stock = relationship("Stock", back_populates="movements")
    user = relationship("User")

