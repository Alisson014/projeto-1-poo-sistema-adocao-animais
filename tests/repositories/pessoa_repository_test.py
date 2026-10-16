from src.domain import Pessoa, Adotante, Cachorro
from src.repositories import PessoaRespository, AnimalRepository

from random import randint
import pytest

adotante_repository = PessoaRespository("tests/data/adotante_teste.json", Adotante)


# Utilizado para a geração dinâmica de emails diferentes (apenas para os testes)
email = f"email{randint(1, 1000000000)}@gmail.com"

adotante = Adotante(
    nome="teste",
    email=email,
    idade=18,
    moradia="CASA_COM_QUINTAL",
    experiencia="INICIANTE",
    tempo_livre_min=50,
    possui_criancas=True,
    outros_animais=True,
    area_util=50,
)

def test_create_adotante():
    assert adotante_repository.create(adotante)

def test_get_all_adotante():
    adotantes = adotante_repository.get_all()
    assert len(adotantes) >= 1
    assert adotantes[-1] == adotante

def test_get_by_email_adotante():
    getted_adotante = adotante_repository.get_by_email(email)

    assert repr(getted_adotante) == repr(adotante)

def test_update_adotante():
    getted_adotante = adotante_repository.get_by_email(email)
    getted_adotante.area_util = 100
    getted_adotante.idade = 21
    getted_adotante.tempo_livre_min = 240
    getted_adotante.experiencia = "AVANCADO"

    adotante_repository.update(getted_adotante)

    new_adotante = adotante_repository.get_by_email(email)

    assert repr(getted_adotante) == repr(new_adotante)

def test_delete_by_email_adotante():
    deleted_email = f"email{randint(1, 1000000000)}@gmail.com"
    deleted_adotante = Adotante(
        nome="teste",
        email=f"{deleted_email}",
        idade=18,
        moradia="CASA_COM_QUINTAL",
        experiencia="INICIANTE",
        tempo_livre_min=50,
        possui_criancas=True,
        outros_animais=True,
        area_util=50,
    )

    adotante_repository.create(deleted_adotante)

    adotante_repository.delete_by_email(deleted_email)

    with pytest.raises(Exception):
        adotante_repository.get_by_email(deleted_email)

