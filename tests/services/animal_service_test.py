from src.domain import Animal, Cachorro, Calopsita, Coelho, Gato, Adotante, Evento
from src.services import AnimalService
from src.domain.exceptions import ValorForaDoIntervaloError, TipagemError, TransicaoDeEstadoInvalidaError, NaoCadastradoError

from datetime import datetime
import pytest

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

evento = Evento(tipo="CONSULTA", descricao="descricao", data=datetime.now())

animal_service = AnimalService("tests/data/animal/cachorro_teste.json", "tests/data/animal/calopsita_teste.json", "tests/data/animal/coelho_teste.json", "tests/data/animal/gato_teste.json")

def test_create():
    data_animal = cachorro.to_dict()
    data_animal.pop("id")

    assert animal_service.create("Cachorro", data_animal)

def test_get_all():
    animais = animal_service.get_all()
    assert len(animais) >= 1

def test_get_all_type_animal():
    cachorros = animal_service.get_all_type_animal("Cachorro")

    assert len(cachorros) >= 1
    assert type(cachorros[0]).__name__ == "Cachorro"

def test_get_by_id():
    animal = animal_service.get_by_id("Cachorro", 1)
    assert type(animal).__name__ == "Cachorro"

def test_update_only_updated_keys():
    animal = animal_service.get_by_id("Cachorro", 1)

    updated_animal_data = {}

    updated_animal_data["nome"] = "Ás atualizado"
    updated_animal_data["passeios_necessarios_dia"] = 2

    res = animal_service.update("Cachorro", updated_animal_data, animal.id)
    assert type(res).__name__ == "Cachorro"

def test_update_all_keys():
    animal = animal_service.get_by_id("Cachorro", 1)

    animal.adicionar_evento(evento)
    updated_animal_data = animal.to_dict()

    updated_animal_data["nome"] = "Ás atualizado"
    updated_animal_data["passeios_necessarios_dia"] = 2

    res = animal_service.update("Cachorro", updated_animal_data, animal.id)
    assert type(res).__name__ == "Cachorro"

def test_update_error_transicao_invalida():
    animal = animal_service.get_by_id("Cachorro", 1)

    updated_animal_data = {}

    updated_animal_data["status"] = "DEVOLVIDO"

    with pytest.raises(TransicaoDeEstadoInvalidaError):
        animal_service.update("Cachorro", updated_animal_data, animal.id)

def test_update_error_tipagem():
    animal = animal_service.get_by_id("Cachorro", 1)

    updated_animal_data = {}

    updated_animal_data["sexo"] = "INVALIDO"

    with pytest.raises(TipagemError):
        animal_service.update("Cachorro", updated_animal_data, animal.id)

def test_update_error_fora_do_intervalo():
    animal = animal_service.get_by_id("Cachorro", 1)

    updated_animal_data = {}

    updated_animal_data["idade_meses"] = -1

    with pytest.raises(ValorForaDoIntervaloError):
        animal_service.update("Cachorro", updated_animal_data, animal.id)

def test_delete_by_id():
    data_animal = cachorro.to_dict()
    data_animal.pop("id")

    deleted_animal = animal_service.create("Cachorro", data_animal)

    animal_service.delete_by_id("Cachorro", deleted_animal.id)

    with pytest.raises(NaoCadastradoError):
        animal_service.get_by_id("Cachorro", deleted_animal.id)

