from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)
    content_type = Column(String)
