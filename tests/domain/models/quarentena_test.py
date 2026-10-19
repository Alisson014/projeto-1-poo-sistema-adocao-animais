from src.domain.models import Quarentena, Cachorro
from src.domain.exceptions import *

from datetime import datetime

import pytest


# Testes Quarentena

cachorro = Cachorro(
    id=0,
    especie="especie",
    nome="Az",
    sexo="MACHO",
    idade_meses=1,
    porte="M",
    status="DISPONIVEL",
    energia="HIPERATIVO",
    cuidado_especial=False,
    data_entrada=datetime.now(),
    historico=[],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    vacinas=[],
    raca="Golden",
    passeios_necessarios_dia=1,
)

def test_cria_quarentena():
    quarentena = Quarentena(
        id= 0, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
    )
    assert quarentena


def test_cria_quarentena_motivo_error():
    with pytest.raises(TipagemError):
        quarentena = Quarentena(
            id= 0, animal=cachorro, data_inicial=datetime.now(), motivo="INVALIDO", status="CUMPRIDA"
        )


def test_cria_quarentena_status_error():
    with pytest.raises(TipagemError):
        quarentena = Quarentena(
            id= 0, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="INVALIDO"
        )
