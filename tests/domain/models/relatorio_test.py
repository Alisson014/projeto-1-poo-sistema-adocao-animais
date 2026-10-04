from src.domain.models import (
    Top5MaisAdotaveis,
    TaxaAdocaoEspecies,
    TaxaAdocaoPorte,
    TaxaTempoMedioEntradaAdocao,
    TaxaDevolucoes,
    Cachorro,
    Adotante,
    Adocao,
    Devolucao,
)
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

adocao = Adocao(
    id=1,
    animal=cachorro,
    adotante=adotante,
    taxa=10,
    pago=False,
    data=datetime.now(),
)

devolucao = Devolucao(
    id=1, animal=cachorro, adotante=adotante, motivo="OUTRO", data=datetime.now()
)


# Testes Top5MaisAdotaveis
def test_cria_Top5MaisAdotaveis():
    top5 = Top5MaisAdotaveis(
        id=1, data=datetime.now(), nome="nome", animais=[], adotantes=[]
    )
    assert top5


def test_cria_Top5MaisAdotaveis_animais():
    top5 = Top5MaisAdotaveis(
        id=1, data=datetime.now(), nome="nome", animais=[cachorro], adotantes=[]
    )
    assert top5


def test_cria_Top5MaisAdotaveis_adotantes():
    top5 = Top5MaisAdotaveis(
        id=1, data=datetime.now(), nome="nome", animais=[cachorro], adotantes=[adotante]
    )
    assert top5


# Testes TaxaAdocaoEspecies
def test_cria_TaxaAdocaoEspecies():
    taxa_adocao = TaxaAdocaoEspecies(id=1, data=datetime.now(), nome="nome", adocoes=[])
    assert taxa_adocao


def test_cria_TaxaAdocaoEspecies_adocoes():
    taxa_adocao = TaxaAdocaoEspecies(
        id=1, data=datetime.now(), nome="nome", adocoes=[adocao]
    )
    assert taxa_adocao


# Testes TaxaAdocaoPorte
def test_cria_TaxaAdocaoPorte():
    taxa_adocao = TaxaAdocaoPorte(id=1, data=datetime.now(), nome="nome", adocoes=[])
    assert taxa_adocao


def test_cria_TaxaAdocaoPorte_adocoes():
    taxa_adocao = TaxaAdocaoPorte(
        id=1, data=datetime.now(), nome="nome", adocoes=[adocao]
    )
    assert taxa_adocao


# Testes TaxaTempoMedioEntradaAdocao
def test_cria_TaxaTempoMedioEntradaAdocao():
    tempo = TaxaTempoMedioEntradaAdocao(
        id=1, data=datetime.now(), nome="nome", adocoes=[]
    )
    assert tempo


def test_cria_TaxaTempoMedioEntradaAdocao_adocoes():
    tempo = TaxaTempoMedioEntradaAdocao(
        id=1, data=datetime.now(), nome="nome", adocoes=[adocao]
    )
    assert tempo


# Testes TaxaDevolucoes
def test_cria_TaxaDevolucoes():
    taxa = TaxaDevolucoes(id=1, data=datetime, nome="nome", adocoes=[], devolucoes=[])
    assert taxa


def test_cria_TaxaDevolucoes_adocoes():
    taxa = TaxaDevolucoes(
        id=1, data=datetime, nome="nome", adocoes=[adocao], devolucoes=[]
    )
    assert taxa


def test_cria_TaxaDevolucoes_devolucoes():
    taxa = TaxaDevolucoes(
        id=1, data=datetime, nome="nome", adocoes=[], devolucoes=[devolucao]
    )
    assert taxa
