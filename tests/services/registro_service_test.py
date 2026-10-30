from src.domain import Animal, Cachorro, Calopsita, Coelho, Gato, Adotante, Adocao
from src.config import PesosCompatibilidade
from src.services import RegistroService
from src.repositories import PessoaRespository, PoliticaRepository
from src.domain.exceptions import ValorForaDoIntervaloError, TipagemError, TransicaoDeEstadoInvalidaError, NaoCadastradoError

from datetime import datetime
import pytest
from random import randint

email = f"email.registro{randint(1, 1000000000)}@gmail.com"

# Dados auxiliares
cachorro = Cachorro(
    id=1,
    especie="especie",
    nome="Az",
    sexo="MACHO",
    idade_meses=1,
    porte="M",
    status="DISPONIVEL",
    energia="HIPERATIVO",
    cuidado_especial=False,
    data_entrada=datetime(2025, 1, 10),
    historico=[],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    vacinas=[],
    raca="Golden",
    passeios_necessarios_dia=1,
)

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

adocao = Adocao(
    id=0,
    animal=cachorro,
    adotante=adotante,
    taxa=10,
    pago=True,
    data=datetime.now(),
)

adotante_path = "tests/data/pessoa/adotante_teste.json"
PessoaRespository(adotante_path, Adotante).create(adotante)
adotante = PessoaRespository(adotante_path, Adotante).get_by_email(email)

politica_repository = PoliticaRepository("tests/data/settings.json")

try: 
    pesos_compatibilidade = PesosCompatibilidade(nome="pesos compatibilidade", data_modificacao=datetime.now(), peso_porte_moradia=0.2, peso_experiencia_temperamento=0.3, peso_tempo_livre_energia=0.2, peso_criancas_temperamento=0.3)
    # Garante 
    politica_repository.create(pesos_compatibilidade)
except Exception:
    # Ignora caso ocorra o erro de política já cadastrada
    pass


politica_repository = PoliticaRepository("tests/data/settings.json")
Pesos:PesosCompatibilidade = politica_repository.get_by_name("PesosCompatibilidade")

registro_service = RegistroService(
    "tests/data/registro/reserva_teste.json",
    "tests/data/registro/reserva_teste.json",
    "tests/data/registro/reserva_teste.json",
    "tests/data/registro/reserva_teste.json",
    "tests/data/registro/devolucao_teste.json",
    "tests/data/registro/devolucao_teste.json",
    "tests/data/registro/devolucao_teste.json",
    "tests/data/registro/devolucao_teste.json",
    "tests/data/registro/adocao_teste.json",
    "tests/data/registro/adocao_teste.json",
    "tests/data/registro/adocao_teste.json",
    "tests/data/registro/adocao_teste.json",
    "tests/data/animal/cachorro_teste.json",
    "tests/data/animal/cachorro_teste.json",
    "tests/data/animal/cachorro_teste.json",
    "tests/data/animal/cachorro_teste.json",
    adotante_path,
)

def test_create():
    registro_data = adocao.to_dict()
    registro_data.pop("id")
    registro_data["animal"] = cachorro.to_dict()
    registro_data["adotante"] = adotante.to_dict()

    assert registro_service.create("Adocao", "Cachorro", registro_data, Pesos)


# Não testados aqui devido à inexistência dos bancos de registros específicos dos demais animais
# No contexto dos testes, existem apenas 

# def test_get_all():
# def test_get_all_type_registro():

def test_get_all_type_registro_type_animal():
    res = registro_service.get_all_type_registro_type_animal("Adocao", "Cachorro")
    assert len(res) >= 1
    assert type(res[0]).__name__ == "Adocao"
    assert type(res[0].animal).__name__ == "Cachorro"

def test_get_by_id():
    res = registro_service.get_by_id("Adocao", "Cachorro", 1)
    assert res
    assert type(res).__name__ == "Adocao"

def test_update_only_updated_keys():
    updated_data = {}

    updated_data["taxa"] = 12

    res = registro_service.update("Adocao", "Cachorro", updated_data, 1)
    assert res

def test_update_all_keys():
    registro = registro_service.get_by_id("Adocao", "Cachorro", 1)
    updated_data = registro.to_dict()

    updated_data["taxa"] = 1234
    res = registro_service.update("Adocao", "Cachorro", updated_data, 1)
    assert res

def test_delete_by_id():
    registro_data = adocao.to_dict()
    registro_data.pop("id")
    registro_data["animal"] = cachorro.to_dict()
    registro_data["adotante"] = adotante.to_dict()

    del_registro = registro_service.create("Adocao", "Cachorro", registro_data, Pesos)

    registro_service.delete_by_id("Adocao", "Cachorro", del_registro.id)

    with pytest.raises(NaoCadastradoError):
        registro_service.get_by_id("Adocao", "Cachorro", del_registro.id)
