from .animal_schema import CachorroResponseSchema, CalopsitaResponseSchema, CoelhoResponseSchema, GatoResponseSchema
from .pessoa_schema import AdotanteSchema

from pydantic import BaseModel, Field
from typing import Literal, Optional, Union
from datetime import datetime


class RegistroSchema(BaseModel):
    animal: CachorroResponseSchema | CalopsitaResponseSchema | CoelhoResponseSchema | GatoResponseSchema = Field(...)
    adotante: AdotanteSchema = Field(...)


# ===========================
# RESERVA
# ===========================

class ReservaCreateSchema(RegistroSchema):
    data_inicial: datetime = Field(...)
    data_expiracao: Optional[datetime] = Field(None)
    status: Literal["ATIVA", "CANCELADA", "EXPIRADA"] = Field(...)
    compatibilidade: float = 0

class ReservaResponseSchema(ReservaCreateSchema):
    id: int

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# ADOCAO
# ===========================

class AdocaoCreateSchema(RegistroSchema):
    pago: bool = Field(...)
    data: datetime = Field(...)
    taxa: float = 0

class AdocaoResponseSchema(AdocaoCreateSchema):
    id: int

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# DEVOLUCAO
# ===========================

class DevolucaoCreateSchema(RegistroSchema):
    motivo: Literal["COMPORTAMENTO", "PESSOAL", "DOENCA", "OUTRO"] = Field(...)
    data: datetime = datetime.now()

class DevolucaoResponseSchema(DevolucaoCreateSchema):
    id: int

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# UNION
# ===========================

RegistroResponseUnion = Union[ReservaResponseSchema, AdocaoResponseSchema, DevolucaoResponseSchema]
