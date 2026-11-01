
from datetime import datetime

from src.domain import Cachorro, Calopsita, Coelho, Gato
from src.domain.models import Quarentena
from src.repositories import QuarentenaRepository, AnimalRepository

from datetime import datetime
from pathlib import Path
import pytest

# Garante que a pasta dos arquivos fictícios existe
Path("tests/data/quarentena").mkdir(parents=True, exist_ok=True)

cachorro_path = "tests/data/quarentena/cachorro_teste.json"
calopsita_path = "tests/data/quarentena/calopsita_teste.json"
coelho_path = "tests/data/quarentena/coelho_teste.json"
gato_path = "tests/data/quarentena/gato_teste.json"


# Testes Quarentena Cachorro

quarentena_cachorro_repository = QuarentenaRepository("tests/data/quarentena/quarentena_cachorro_teste.json", Cachorro, cachorro_path)

cachorro_repo = AnimalRepository(cachorro_path, Cachorro)

quarentena_cacho_id = quarentena_cachorro_repository.generate_id()

cachorro = Cachorro(
    id=cachorro_repo.generate_id(),
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

cachorro_repo.create(cachorro)

quarentena_cachorro = Quarentena(
    id=quarentena_cacho_id, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
)

def test_gera_id_quarentena_cachorro():
    assert quarentena_cacho_id == quarentena_cachorro.id

def test_create_quarentena_cachorro():
    assert quarentena_cachorro_repository.create(quarentena_cachorro)

def test_get_all_quarentena_cachorro():
    quarentenas = quarentena_cachorro_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_cachorro():
    getted_quarentena = quarentena_cachorro_repository.get_by_id(quarentena_cacho_id)
    assert type(getted_quarentena.animal).__name__ == "Cachorro"

def test_update_quarentena_cachorro():
    getted_quarentena = quarentena_cachorro_repository.get_by_id(quarentena_cacho_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_cachorro_repository.update(getted_quarentena)

    new_quarentena = quarentena_cachorro_repository.get_by_id(quarentena_cacho_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_cachorro():
    deleted_id = quarentena_cachorro_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
    )

    quarentena_cachorro_repository.create(deleted_quarentena)

    quarentena_cachorro_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_cachorro_repository.get_by_id(deleted_quarentena.id)


# Testes Quarentena calopsita

quarentena_calopsita_repository = QuarentenaRepository("tests/data/quarentena/quarentena_calopsita_teste.json", Calopsita, calopsita_path)

quarentena_calop_id = quarentena_calopsita_repository.generate_id()

calopsita_repo = AnimalRepository(calopsita_path, Calopsita)

calopsita = Calopsita(
    id=calopsita_repo.generate_id(),
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

calopsita_repo.create(calopsita)

quarentena_calopsita = Quarentena(
    id= quarentena_calop_id, animal=calopsita, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
)

def test_gera_id_quarentena_calopsita():
    assert quarentena_calop_id == quarentena_calopsita.id

def test_create_quarentena_calopsita():
    assert quarentena_calopsita_repository.create(quarentena_calopsita)

def test_get_all_quarentena_calopsita():
    quarentenas = quarentena_calopsita_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_calopsita():
    getted_quarentena = quarentena_calopsita_repository.get_by_id(quarentena_calop_id)
    assert type(getted_quarentena.animal).__name__ == "Calopsita"

def test_update_quarentena_calopsita():
    getted_quarentena = quarentena_calopsita_repository.get_by_id(quarentena_calop_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_calopsita_repository.update(getted_quarentena)

    new_quarentena = quarentena_calopsita_repository.get_by_id(quarentena_calop_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_calopsita():
    deleted_id = quarentena_calopsita_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=calopsita, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
    )

    quarentena_calopsita_repository.create(deleted_quarentena)

    quarentena_calopsita_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_calopsita_repository.get_by_id(deleted_quarentena.id)


# Testes Quarentena coelho

quarentena_coelho_repository = QuarentenaRepository("tests/data/quarentena/quarentena_coelho_teste.json", Coelho, coelho_path)

quarentena_coel_id = quarentena_coelho_repository.generate_id()

coelho_repo = AnimalRepository(coelho_path, Coelho)

coelho = Coelho(
    id=coelho_repo.generate_id(),
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

coelho_repo.create(coelho)

quarentena_coelho = Quarentena(
    id= quarentena_coel_id, animal=coelho, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
)

def test_gera_id_quarentena_coelho():
    assert quarentena_coel_id == quarentena_coelho.id

def test_create_quarentena_coelho():
    assert quarentena_coelho_repository.create(quarentena_coelho)

def test_get_all_quarentena_coelho():
    quarentenas = quarentena_coelho_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_coelho():
    getted_quarentena = quarentena_coelho_repository.get_by_id(quarentena_coel_id)
    assert type(getted_quarentena.animal).__name__ == "Coelho"

def test_update_quarentena_coelho():
    getted_quarentena = quarentena_coelho_repository.get_by_id(quarentena_coel_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_coelho_repository.update(getted_quarentena)

    new_quarentena = quarentena_coelho_repository.get_by_id(quarentena_coel_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_coelho():
    deleted_id = quarentena_coelho_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=coelho, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
    )

    quarentena_coelho_repository.create(deleted_quarentena)

    quarentena_coelho_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_coelho_repository.get_by_id(deleted_quarentena.id)


# Testes Quarentena gato

quarentena_gato_repository = QuarentenaRepository("tests/data/quarentena/quarentena_gato_teste.json", Gato, gato_path)

quarentena_gato_id = quarentena_gato_repository.generate_id()

gato_repo = AnimalRepository(gato_path, Gato)

gato = Gato(
    id=gato_repo.generate_id(),
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

quarentena_gato = Quarentena(
    id= quarentena_gato_id, animal=gato, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
)

gato_repo.create(gato)

def test_gera_id_quarentena_gato():
    assert quarentena_gato_id == quarentena_gato.id

def test_create_quarentena_gato():
    assert quarentena_gato_repository.create(quarentena_gato)

def test_get_all_quarentena_gato():
    quarentenas = quarentena_gato_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_gato():
    getted_quarentena = quarentena_gato_repository.get_by_id(quarentena_gato_id)
    assert type(getted_quarentena.animal).__name__ == "Gato"

def test_update_quarentena_gato():
    getted_quarentena = quarentena_gato_repository.get_by_id(quarentena_gato_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_gato_repository.update(getted_quarentena)

    new_quarentena = quarentena_gato_repository.get_by_id(quarentena_gato_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_gato():
    deleted_id = quarentena_gato_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=gato, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
    )

    quarentena_gato_repository.create(deleted_quarentena)

    quarentena_gato_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_gato_repository.get_by_id(deleted_quarentena.id)

