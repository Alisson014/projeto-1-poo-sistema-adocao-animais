from .animal_schema import CachorroResponseSchema, CalopsitaResponseSchema, CoelhoResponseSchema, GatoResponseSchema

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class QuarentenaCreateSchema(BaseModel):
    animal: CachorroResponseSchema | CalopsitaResponseSchema | CoelhoResponseSchema | GatoResponseSchema = Field(...)
    data_inicial: datetime = Field(...)
    data_final: datetime | None = None
    motivo: Literal["COMPORTAMENTO", "DOENCA", "OUTRO"] = Field(...)
    status: Literal["ATIVA", "CUMPRIDA"] = Field(...)

class QuarentenaResponseSchema(QuarentenaCreateSchema):
    id: int = Field(...)

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True
