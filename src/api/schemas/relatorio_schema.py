from .animal_schema import AnimalResponseUnion
from .pessoa_schema import AdotanteSchema
from .registro_schema import AdocaoResponseSchema, DevolucaoResponseSchema

from pydantic import BaseModel, Field
from typing import Literal, Optional, Union
from datetime import datetime


class RelatorioSchema(BaseModel):
    data: datetime = Field(...)
    nome: str = Field(...)


# ===========================
# TOP 5 MAIS ADOTAVEIS
# ===========================

class Top5MaisAdotaveisCreateSchema(RelatorioSchema):
    animais: list[AnimalResponseUnion] = Field(...)
    adotantes: list[AdotanteSchema] = Field(...)
    
class Top5MaisAdotaveisResponseSchema(Top5MaisAdotaveisCreateSchema):
    id: int
    top5: list[AnimalResponseUnion]

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# TAXA ADOCAO ESPECIES/PORTE
# ===========================

class TaxaAdocaoCreateSchema(RelatorioSchema): # Também utilizado para TEMPO MEDIO ENTRADA ADOCAO
    adocoes: list[AdocaoResponseSchema] = Field(...)

class TaxaAdocaoResponseSchema(TaxaAdocaoCreateSchema):
    id: int
    taxas: dict

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# TEMPO MEDIO ENTRADA ADOCAO
# ===========================

class TaxaTempoMedioEntradaAdocaoResponseSchema(TaxaAdocaoCreateSchema):
    id: int
    tempo_medio_meses: int | float
    
    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# TAXA DEVOLUCOES
# ===========================

class TaxaDevolucoesCreateSchema(RelatorioSchema):
    adocoes: list[AdocaoResponseSchema] = Field(...)
    devolucoes: list[DevolucaoResponseSchema] = Field(...)

class TaxaDevolucoesResponseSchema(TaxaDevolucoesCreateSchema):
    id: int
    taxa: str

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# UNION
# ===========================

RelatorioResponseUnion = Union[Top5MaisAdotaveisResponseSchema, TaxaAdocaoResponseSchema, TaxaTempoMedioEntradaAdocaoResponseSchema, TaxaDevolucoesResponseSchema]

RelatorioCreateUnion = Union[Top5MaisAdotaveisCreateSchema, TaxaAdocaoCreateSchema, TaxaDevolucoesCreateSchema]
