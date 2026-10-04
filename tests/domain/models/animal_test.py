from src.domain.models import Cachorro, Calopsita, Coelho, Gato
from src.domain.exceptions import *
from datetime import datetime

import pytest


# Testes em Cachorro
def test_cria_cachorro():
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
    assert cachorro


def test_cria_cachorro_erro_sexo():
    with pytest.raises(TipagemError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="INVALIDO",
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


def test_cria_cachorro_erro_idade_meses():
    with pytest.raises(ValorForaDoIntervaloError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="FEMEA",
            idade_meses=-1,
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


def test_cria_cachorro_erro_porte():
    with pytest.raises(TipagemError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="MACHO",
            idade_meses=1,
            porte="INVALIDO",
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


def test_cria_cachorro_erro_status():
    with pytest.raises(TipagemError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="MACHO",
            idade_meses=1,
            porte="M",
            status="INVALIDO",
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


def test_cria_cachorro_erro_energia():
    with pytest.raises(TipagemError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="MACHO",
            idade_meses=1,
            porte="M",
            status="ADOTADO",
            energia="INVALIDO",
            cuidado_especial=False,
            data_entrada=datetime.now(),
            historico=[],
            temperamento=["DOCIL"],
            nivel_adestramento=1,
            vacinas=[],
            raca="Golden",
            passeios_necessarios_dia=1,
        )


def test_cria_cachorro_erro_temperamento():
    with pytest.raises(TipagemError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="MACHO",
            idade_meses=1,
            porte="M",
            status="ADOTADO",
            energia="CALMO",
            cuidado_especial=False,
            data_entrada=datetime.now(),
            historico=[],
            temperamento=["DOCIL", "INVALIDO"],
            nivel_adestramento=1,
            vacinas=[],
            raca="Golden",
            passeios_necessarios_dia=1,
        )


def test_cria_cachorro_erro_nivel_adestramento():
    with pytest.raises(ValorForaDoIntervaloError):
        cachorro = Cachorro(
            id=0,
            especie="especie",
            nome="Az",
            sexo="MACHO",
            idade_meses=1,
            porte="M",
            status="ADOTADO",
            energia="CALMO",
            cuidado_especial=False,
            data_entrada=datetime.now(),
            historico=[],
            temperamento=["DOCIL"],
            nivel_adestramento=-1,
            vacinas=[],
            raca="Golden",
            passeios_necessarios_dia=1,
        )


def test_cria_cachorro_erro_trasicao_status():
    with pytest.raises(TransicaoDeEstadoInvalidaError):
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
        cachorro.status = "DEVOLVIDO"


# Testes em Calopsita
def test_cria_calopsita():
    calopsita = Calopsita(
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
        canta=False,
    )
    assert calopsita


# Testes em Coelho
def test_cria_coelho():
    coelho = Coelho(
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
        tamanho_gaiola_m3=1,
    )
    assert coelho


# Testes em Gato
def test_cria_gato():
    gato = Gato(
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
        independencia=True,
    )
    assert gato
