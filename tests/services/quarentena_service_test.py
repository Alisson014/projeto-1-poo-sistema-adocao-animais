from src.domain import Cachorro, Quarentena
from src.repositories import QuarentenaRepository
from src.services import QuarentenaService
from src.domain.exceptions import ValorForaDoIntervaloError, TipagemError, TransicaoDeEstadoInvalidaError, NaoCadastradoError

from datetime import datetime
import pytest

cachorro_path = "tests/data/animal/cachorro_teste.json"
calopsita_path = "tests/data/animal/calopsita_teste.json"
coelho_path = "tests/data/animal/coelho_teste.json"
gato_path = "tests/data/animal/gato_teste.json"


# Dados auxiliares

quarentena_cachorro_repository = QuarentenaRepository("tests/data/quarentena/quarentena_cachorro_teste.json", Cachorro, cachorro_path)

quarentena_cacho_id = quarentena_cachorro_repository.generate_id()

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
    data_entrada=datetime.now(),
    historico=[],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    vacinas=[],
    raca="Golden",
    passeios_necessarios_dia=1,
)

quarentena = Quarentena(
    id= quarentena_cacho_id, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
)

quarentena_service = QuarentenaService(
    "tests/data/quarentena/quarentena_cachorro_teste.json",
    "tests/data/quarentena/quarentena_calopsita_teste.json",
    "tests/data/quarentena/quarentena_coelho_teste.json",
    "tests/data/quarentena/quarentena_gato_teste.json",
    "tests/data/animal/cachorro_teste.json",
    "tests/data/animal/calopsita_teste.json",
    "tests/data/animal/coelho_teste.json",
    "tests/data/animal/gato_teste.json",
    )

def test_create():
    quarentena_data = quarentena.to_dict()
    quarentena_data.pop("id")
    quarentena_data["animal"] = cachorro.to_dict()

    assert quarentena_service.create("Cachorro", quarentena_data)

def test_get_all():
    quarentenas = quarentena_service.get_all()
    assert len(quarentenas) >= 1

def test_get_all_type_animal():
    quarentenas = quarentena_service.get_all_type_animal("Cachorro")
    assert len(quarentenas) >= 1
    assert type(quarentenas[0]).__name__ == "Quarentena"
    assert type(quarentenas[0].animal).__name__ == "Cachorro"

def test_get_by_id():
    quarentena = quarentena_service.get_by_id("Cachorro", quarentena_cacho_id)
    assert type(quarentena).__name__ == "Quarentena"

def test_update_only_updated_keys():
    updated_quarentena_data = {}

    updated_quarentena_data["status"] = "CUMPRIDA"

    res = quarentena_service.update("Cachorro", updated_quarentena_data, quarentena_cacho_id)
    assert type(res).__name__ == "Quarentena"

def test_update_all_keys():
    updated_quarentena_data = quarentena.to_dict()

    updated_quarentena_data["data_final"] = datetime.now()
    updated_quarentena_data["status"] = "CUMPRIDA"
    updated_quarentena_data["motivo"] = "COMPORTAMENTO"
    res = quarentena_service.update("Cachorro", updated_quarentena_data, quarentena_cacho_id)
    assert type(res).__name__ == "Quarentena"
    
def test_delete_by_id():
    del_quarentena = Quarentena(
        id=1, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
    )

    data = del_quarentena.to_dict()
    data["animal"] = cachorro.to_dict()
    data.pop("id")

    deleted = quarentena_service.create("Cachorro", data)

    quarentena_service.delete_by_id("Cachorro", deleted.id)

    with pytest.raises(NaoCadastradoError):
        quarentena_service.get_by_id("Cachorro", deleted.id)
