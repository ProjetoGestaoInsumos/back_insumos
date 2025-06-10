from sqlalchemy import Column, Integer, String, Enum
from app.database.db import Base
import enum

class UnitEnum(enum.Enum):
    unidade = "unidade"
    g = "g"
    kg = "kg"
    mg = "mg"
    mcg = "mcg"
    ml = "ml"
    l = "l"
    colher = "colher"
    colher_cha = "colher de chá"
    colher_sopa = "colher de sopa"
    xicara = "xícara"
    pacote = "pacote"
    caixa = "caixa"
    frasco = "frasco"
    ampola = "ampola"
    tubo = "tubo"
    barra = "barra"
    fatia = "fatia"
    folha = "folha"
    pitada = "pitada"
    outros = "outros"

class CategoryEnum(enum.Enum):
    carnes = "carnes"
    aves = "aves"
    peixes_frutos_do_mar = "peixes e frutos do mar"
    laticinios = "laticínios"
    graos_cereais = "grãos e cereais"
    massas = "massas"
    legumes = "legumes"
    verduras = "verduras"
    frutas = "frutas"
    temperos_especiarias = "temperos e especiarias"
    oleos_gorduras = "óleos e gorduras"
    doces_sobremesas = "doces e sobremesas"
    bebidas = "bebidas"
    paes_panificacao = "pães e panificação"
    molhos_caldos = "molhos e caldos"
    congelados = "congelados"
    enlatados = "enlatados"
    farinhas = "farinhas"
    conservas = "conservas"
    snacks = "snacks"
    condimentos = "condimentos"
    cereais_matinais = "cereais matinais"
    embutidos = "embutidos"
    confeitaria = "confeitaria"
    produtos_limpeza = "produtos de limpeza"
    outros = "outros"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unit = Column(Enum(UnitEnum), nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    description = Column(String)