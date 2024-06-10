from pydantic import BaseModel

class User(BaseModel):
    id: int
    nome: str
    email: str
