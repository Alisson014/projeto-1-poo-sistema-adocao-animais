from src.domain.models import Adotante, Cachorro
from src.domain.exceptions import *

from datetime import datetime

import pytest


# Testes Adotante
def test_cria_adotante():
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
    assert adotante


def test_cria_adotante_email_error():
    with pytest.raises(EmailInvalidoError):
        adotante = Adotante(
            nome="teste",
            email="emailgmailcom",
            idade=18,
            moradia="CASA_COM_QUINTAL",
            experiencia="AVANCADO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )


def test_cria_adotante_email2_error():
    with pytest.raises(EmailInvalidoError):
        adotante = Adotante(
            nome="teste",
            email="",
            idade=18,
            moradia="CASA_COM_QUINTAL",
            experiencia="AVANCADO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )


def test_cria_adotante_idade_error():
    with pytest.raises(ValorForaDoIntervaloError):
        adotante = Adotante(
            nome="teste",
            email="email@gmail.com",
            idade=-18,
            moradia="CASA_COM_QUINTAL",
            experiencia="AVANCADO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )


def test_cria_adotante_moradia_error():
    with pytest.raises(TipagemError):
        adotante = Adotante(
            nome="teste",
            email="email@gmail.com",
            idade=18,
            moradia="INVALIDO",
            experiencia="AVANCADO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )


def test_cria_adotante_experiencia_error():
    with pytest.raises(TipagemError):
        adotante = Adotante(
            nome="teste",
            email="email@gmail.com",
            idade=18,
            moradia="CASA_COM_QUINTAL",
            experiencia="INVALIDO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )


def test_cria_adotante_tempo_livre_error():
    with pytest.raises(ValorForaDoIntervaloError):
        adotante = Adotante(
            nome="teste",
            email="email@gmail.com",
            idade=18,
            moradia="CASA_COM_QUINTAL",
            experiencia="AVANCADO",
            tempo_livre_min=-50,
            possui_criancas=True,
            outros_animais=True,
            area_util=50,
        )


def test_cria_adotante_area_util_error():
    with pytest.raises(ValorForaDoIntervaloError):
        adotante = Adotante(
            nome="teste",
            email="email@gmail.com",
            idade=18,
            moradia="CASA_COM_QUINTAL",
            experiencia="AVANCADO",
            tempo_livre_min=50,
            possui_criancas=True,
            outros_animais=True,
            area_util=-50,
        )
