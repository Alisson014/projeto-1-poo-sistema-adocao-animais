from pydantic import BaseModel, Field
from typing import Union
from datetime import datetime


class PoliticaSchema(BaseModel):
    nome: str = Field(..., min_length=2)
    data_modificacao: datetime | str = datetime.now()

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True

# ===========================
# IDADE MINIMA
# ===========================

class IdadeMinimaSchema(PoliticaSchema):
    idade_minima: int = Field(..., ge=0)


# ===========================
# PORTE X AREA
# ===========================

class PorteXAreaSchema(PoliticaSchema):
    porte_p_min: float = Field(..., ge=0)
    porte_m_min: float = Field(..., ge=0)
    porte_g_min: float = Field(..., ge=0)


# ===========================
# DURACAO RESERVA
# ===========================

class DuracaoReservaSchema(PoliticaSchema):
    duracao_dias: int = Field(...)


# ===========================
# PESOS COMPATIBILIDADE
# ===========================

class PesosCompatibilidadeSchema(PoliticaSchema):
    peso_porte_moradia: float = Field(..., ge=0, le=1)
    peso_experiencia_temperamento: float = Field(..., ge=0, le=1)
    peso_tempo_livre_energia: float = Field(..., ge=0, le=1)
    peso_criancas_temperamento: float = Field(..., ge=0, le=1)


# ===========================
# UNION
# ===========================

PoliticaUnion = Union[IdadeMinimaSchema, PorteXAreaSchema, DuracaoReservaSchema, PesosCompatibilidadeSchema]

