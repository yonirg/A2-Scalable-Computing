from pydantic import BaseModel

class Product(BaseModel):
    nome: str
    preco_atual: float
    economia_percentual: float
