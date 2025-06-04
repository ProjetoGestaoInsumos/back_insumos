from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine
from app.api import auth, items, stock, recipe

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API online 🚀"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(stock.router)
app.include_router(recipe.router)