from sqlalchemy import Column, Integer, ForeignKey, String, JSON, Date
from database import Base

class POP(Base):
    __tablename__ = "pop"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    n_students = Column(Integer, nullable=False)
    n_groups = Column(Integer, nullable=False)
    extra_items = Column(JSON, nullable=True)  # item_id e quantity
    objective = Column(String, nullable=True)
    date = Column(Date, nullable=True)
