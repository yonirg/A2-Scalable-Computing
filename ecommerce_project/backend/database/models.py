from sqlalchemy import Column, Integer, String, Float
from .connection import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco_atual = Column(Float)
    economia_percentual = Column(Float)

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, index=True)
