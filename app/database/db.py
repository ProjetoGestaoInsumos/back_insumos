
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = "postgresql://db_insumosge_user:yFTw4r4XPkHR2wlOafB1Daa7LHB5g54x@dpg-d0iu4024d50c73dvp930-a.ohio-postgres.render.com/db_insumosge"

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from app.models import image 
    Base.metadata.create_all(bind=engine)