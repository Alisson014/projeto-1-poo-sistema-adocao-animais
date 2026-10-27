from src.domain import Pessoa, Adotante
from src.services import PessoaService
from src.domain.exceptions import PoliticaError, NaoCadastradoError

from random import randint
import pytest

# Dados auxiliares
email = f"email{randint(1, 1000000000)}@gmail.com"

adotante = Adotante(
    nome="teste service",
    email=email,
    idade=18,
    moradia="CASA_COM_QUINTAL",
    experiencia="INICIANTE",
    tempo_livre_min=50,
    possui_criancas=True,
    outros_animais=True,
    area_util=50,
)

pessoa_service = PessoaService("tests/data/pessoa/adotante_teste.json", "tests/data/settings.json")

def test_create():
    pessoa_data = adotante.to_dict()
    assert pessoa_service.create("Adotante", pessoa_data)

def test_create_Politica_error():
    pessoa_data = adotante.to_dict()
    pessoa_data["idade"] = 10

    with pytest.raises(PoliticaError):
        pessoa_service.create("Adotante", pessoa_data)

def test_get_all():
    adotantes = pessoa_service.get_all()
    assert len(adotantes) >= 1
    assert type(adotantes[0]).__name__ == "Adotante"

def test_get_by_email():
    pessoa = pessoa_service.get_by_email("Adotante", email)
    assert type(pessoa).__name__ == "Adotante"

def test_update_only_updated_keys():
    updated_pessoa = {}
    updated_pessoa["nome"] = "teste service atualizado only keys"

    assert pessoa_service.update("Adotante", updated_pessoa, email)
    
def test_update_all_keys():
    updated_pessoa = adotante.to_dict()
    updated_pessoa["nome"] = "teste service atualizado all keys"
    updated_pessoa["idade"] = 21

    assert pessoa_service.update("Adotante", updated_pessoa, email)

def test_update_Politica_error():
    updated_pessoa = {}
    updated_pessoa["idade"] = 10

    with pytest.raises(PoliticaError):
        pessoa_service.update("Adotante", updated_pessoa, email)

def test_delete_by_email():
    deleted_email = f"del_email{randint(1, 1000000000)}@gmail.com"
    del_adotante = Adotante(
        nome="teste service",
        email=deleted_email,
        idade=18,
        moradia="CASA_COM_QUINTAL",
        experiencia="INICIANTE",
        tempo_livre_min=50,
        possui_criancas=True,
        outros_animais=True,
        area_util=50,
    )

    pessoa_service.create("Adotante", del_adotante.to_dict())

    pessoa_service.delete_by_email("Adotante", deleted_email)

    with pytest.raises(NaoCadastradoError):
        pessoa_service.get_by_email("Adotante", deleted_email)