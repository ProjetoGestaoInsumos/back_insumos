from sqlalchemy import Column, Integer, String, JSON
from app.database.db import Base

class Recipe(Base):
    __tablename__ = "recipe"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    ingredients = Column(JSON, nullable=False)  