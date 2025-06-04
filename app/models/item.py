from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unit = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)