from src.domain.models import EntradaFila, FilaEspera, Adotante, Cachorro
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


# Testes de EntradaFila
def test_cria_entrada_fila():
    entrada = EntradaFila(adotante=adotante, tempo_espera=5, compatibilidade=100)
    assert entrada


# Testes de FilaEspera
def test_cria_fila_espera():
    fila_espera = FilaEspera(animal=cachorro, fila=[])
    assert fila_espera


def test_fila_espera_adiciona_entrada():
    fila_espera = FilaEspera(animal=cachorro, fila=[])
    fila_espera.add(adotante=adotante)
    assert len(fila_espera.get_fila()) == 1


def test_fila_espera_remove_entrada():
    fila_espera = FilaEspera(animal=cachorro, fila=[])
    fila_espera.add(adotante=adotante)
    print(fila_espera.get_fila())
    fila_espera.remove(adotante=adotante)
    assert len(fila_espera.get_fila()) == 0


def test_fila_espera_remove_entrada_error():
    with pytest.raises(NaoEncontradoError):
        fila_espera = FilaEspera(animal=cachorro, fila=[])
        fila_espera.add(adotante=adotante)
        adotante2 = Adotante(
            nome="teste",
            email="email2@gmail.com",
            idade=18,
            moradia="CASA_COM_QUINTAL",
            experiencia="AVANCADO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )
        fila_espera.remove(adotante=adotante2)
