from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine, create_tables
from app.api import auth, resources, upload, media, test_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(resources.router, prefix="/items")
app.include_router(upload.router, prefix="/files") 
app.include_router(media.router, prefix="/files")
app.include_router(test_db.router, prefix="/api")

create_tables()

