
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class EventoSchame(BaseModel):
    tipo: Literal["VACINA", "ADOCAO", "DEVOLUCAO", "QUARENTENA", "CONSULTA"] = Field(...)
    descricao: str = Field(...)
    data: datetime | str = Field(...)

class VacinaSchema(BaseModel):
    nome: str = Field(...)
    data: datetime | str = Field(...)
