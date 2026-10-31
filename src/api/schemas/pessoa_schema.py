from pydantic import BaseModel, Field
from typing import Literal, Union
from datetime import datetime


class PessoaSchema(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$') #Validação para email
    idade: int = Field(..., gt=0)


# ===========================
# ADOTANTE
# ===========================

class AdotanteSchema(PessoaSchema):
    moradia: Literal["APARTAMENTO_COM_VARANDA", "APARTAMENTO_SEM_VARANDA", "CASA_COM_QUINTAL", "CASA_SEM_QUINTA."] = Field(...)
    experiencia: Literal["INICIANTE", "INTERMEDIARIO", "AVANCADO"] = Field(...)
    tempo_livre_min: int = Field(..., ge=0)
    possui_criancas: bool = Field(...)
    outros_animais: bool = Field(...)
    area_util: float = Field(..., ge=0)

