from src.domain.models import Reserva, Adocao, Devolucao, Cachorro, Adotante
from src.domain.exceptions import *

from datetime import datetime

import pytest

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

adotante = Adotante(
    nome="teste",
    email="email@gmail.com",
    idade=18,
    moradia="CASA_COM_QUINTAL",
    experiencia="AVANCADO",
    tempo_livre_min=50,
    possui_criancas=True,
    outros_animais=True,
    area_util=50,
)


# Testes Reserva
def test_cria_reserva():
    reserva = Reserva(
        id=1,
        animal=cachorro,
        adotante=adotante,
        data_inicial=datetime.now(),
        data_expiracao=datetime.now(),
        status="ATIVA",
        compatibilidade=100,
    )
    assert reserva


def test_cria_reserva_status_error():
    with pytest.raises(TipagemError):
        reserva = Reserva(
            id=1,
            animal=cachorro,
            adotante=adotante,
            data_inicial=datetime.now(),
            data_expiracao=datetime.now(),
            status="INVALIDO",
            compatibilidade=100,
        )


# Testes Adocao
def test_cria_adocao():
    adocao = Adocao(
        id=1,
        animal=cachorro,
        adotante=adotante,
        taxa=10,
        pago=False,
        data=datetime.now(),
    )
    assert adocao


# Testes Devolucao
def test_cria_devolucao():
    devolucao = Devolucao(
        id=1, animal=cachorro, adotante=adotante, motivo="OUTRO", data=datetime.now()
    )
    assert devolucao


def test_cria_devolucao_motivo_error():
    with pytest.raises(TipagemError):
        devolucao = Devolucao(
            id=1,
            animal=cachorro,
            adotante=adotante,
            motivo="INVALIDO",
            data=datetime.now(),
        )
