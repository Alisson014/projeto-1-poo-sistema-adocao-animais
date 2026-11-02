from .pessoa_schema import AdotanteSchema
from .animal_schema import AnimalResponseUnion

from pydantic import BaseModel, Field
from typing import Literal, Optional, Union
from datetime import datetime


# ===========================
# ENTRADA FILA
# ===========================

class EntradaFilaSchema(BaseModel):
    adotante: AdotanteSchema = Field(...)
    compatibilidade: float = Field(...)
    data_expiracao: datetime = Field(...)
    data_inicial: datetime = Field(...)

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# FILA ESPERA
# ===========================

class FilaEsperaSchema(BaseModel):
    animal: AnimalResponseUnion = Field(...)
    fila: list[EntradaFilaSchema]
    duracao_reserva: int

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True
