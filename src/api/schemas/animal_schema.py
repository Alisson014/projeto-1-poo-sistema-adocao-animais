from .auxiliares_schema import EventoSchame, VacinaSchema

from pydantic import BaseModel, Field
from typing import Literal, Union
from datetime import datetime

class AnimalCreateSchema(BaseModel):
    especie: str = Field(..., description="Ex: Canis lupus familiaris")
    nome: str = Field(..., min_length=2, max_length=100)
    sexo: Literal["MACHO", "FEMEA"] = Field(..., description="MACHO | FEMEA")
    idade_meses: int = Field(..., ge=0)
    porte: Literal["P", "M", "G"] = Field(..., description="P | M | G")
    status: Literal["DISPONIVEL", "RESERVADO", "ADOTADO", "DEVOLVIDO", "QUARENTENA", "INADOTAVEL"] = Field(..., description="DISPONIVEL RESERVADO ADOTADO DEVOLVIDO QUARENTENA INADOTAVEL")
    energia: Literal["CALMO", "HIPERATIVO"] = Field(..., description="CALMO | HIPERATIVO")
    cuidado_especial: bool = Field(...)
    data_entrada: datetime | str = datetime.now()
    historico: list[EventoSchame] = []
    temperamento: list[str] = []



# ===========================
# CACHORO
# ===========================

class CachorroCreateSchema(AnimalCreateSchema):
    nivel_adestramento: int = Field(..., ge=0, le=3)
    vacinas: list[VacinaSchema] = []
    raca: str = Field(..., description="Golden")
    passeios_necessarios_dia: int = Field(..., ge=0)

class CachorroResponseSchema(CachorroCreateSchema):
    id: int

    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# CALOPSITA
# ===========================

class CalopsitaCreateSchema(AnimalCreateSchema):
    nivel_adestramento: int = Field(..., ge=0, le=3)
    canta: bool

class CalopsitaResponseSchema(CalopsitaCreateSchema):
    id: int
    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# COELHO
# ===========================

class CoelhoCreateSchema(AnimalCreateSchema):
    nivel_adestramento: int = Field(..., ge=0, le=3)
    vacinas: list[VacinaSchema] = []
    raca: str
    tamanho_gaiola_m3: float = Field(..., ge=0.35)

class CoelhoResponseSchema(CoelhoCreateSchema):
    id: int
    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# GATO
# ===========================

class GatoCreateSchema(AnimalCreateSchema):
    nivel_adestramento: int = Field(..., ge=0, le=3)
    vacinas: list[VacinaSchema] = []
    raca: str
    independencia: bool

class GatoResponseSchema(GatoCreateSchema):
    id: int
    class Config:
        # Permite converter models do SQLAlchemy/customizados se necessário
        from_attributes = True


# ===========================
# RESPONSE
# ===========================

AnimalResponseUnion = Union[CachorroResponseSchema, CalopsitaResponseSchema, CoelhoResponseSchema, GatoResponseSchema]
