
from datetime import datetime

from src.domain import Cachorro, Calopsita, Coelho, Gato
from src.domain.models import Quarentena
from src.repositories import QuarentenaRepository
from datetime import datetime

import pytest

cachorro_path = "tests/data/animal/cachorro_teste.json"
calopsita_path = "tests/data/animal/calopsita_teste.json"
coelho_path = "tests/data/animal/coelho_teste.json"
gato_path = "tests/data/animal/gato_teste.json"


# Testes Quarentena Cachorro

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

def test_gera_id_quarentena_cachorro():
    assert quarentena_cacho_id == quarentena.id

def test_create_quarentena_cachorro():
    assert quarentena_cachorro_repository.create(quarentena)

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
        id=deleted_id, animal=cachorro, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
    )

    quarentena_cachorro_repository.create(deleted_quarentena)

    quarentena_cachorro_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_cachorro_repository.get_by_id(deleted_quarentena.id)


# Testes Quarentena calopsita

quarentena_calopsita_repository = QuarentenaRepository("tests/data/quarentena/quarentena_calopsita_teste.json", Calopsita, calopsita_path)

quarentena_calop_id = quarentena_calopsita_repository.generate_id()

calopsita = Calopsita(
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
    canta=False,
)

quarentena = Quarentena(
    id= quarentena_calop_id, animal=calopsita, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
)

def test_gera_id_quarentena_calopsita():
    assert quarentena_calop_id == quarentena.id

def test_create_quarentena_calopsita():
    assert quarentena_calopsita_repository.create(quarentena)

def test_get_all_quarentena_calopsita():
    quarentenas = quarentena_calopsita_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_calopsita():
    getted_quarentena = quarentena_calopsita_repository.get_by_id(quarentena_cacho_id)
    assert type(getted_quarentena.animal).__name__ == "Calopsita"

def test_update_quarentena_calopsita():
    getted_quarentena = quarentena_calopsita_repository.get_by_id(quarentena_cacho_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_calopsita_repository.update(getted_quarentena)

    new_quarentena = quarentena_calopsita_repository.get_by_id(quarentena_cacho_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_calopsita():
    deleted_id = quarentena_calopsita_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=calopsita, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
    )

    quarentena_calopsita_repository.create(deleted_quarentena)

    quarentena_calopsita_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_calopsita_repository.get_by_id(deleted_quarentena.id)


# Testes Quarentena coelho

quarentena_coelho_repository = QuarentenaRepository("tests/data/quarentena/quarentena_coelho_teste.json", Coelho, coelho_path)

quarentena_coel_id = quarentena_coelho_repository.generate_id()

coelho = Coelho(
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
    tamanho_gaiola_m3=1,
)

quarentena = Quarentena(
    id= quarentena_coel_id, animal=coelho, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
)

def test_gera_id_quarentena_coelho():
    assert quarentena_coel_id == quarentena.id

def test_create_quarentena_coelho():
    assert quarentena_coelho_repository.create(quarentena)

def test_get_all_quarentena_coelho():
    quarentenas = quarentena_coelho_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_coelho():
    getted_quarentena = quarentena_coelho_repository.get_by_id(quarentena_cacho_id)
    assert type(getted_quarentena.animal).__name__ == "Coelho"

def test_update_quarentena_coelho():
    getted_quarentena = quarentena_coelho_repository.get_by_id(quarentena_cacho_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_coelho_repository.update(getted_quarentena)

    new_quarentena = quarentena_coelho_repository.get_by_id(quarentena_cacho_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_coelho():
    deleted_id = quarentena_coelho_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=coelho, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
    )

    quarentena_coelho_repository.create(deleted_quarentena)

    quarentena_coelho_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_coelho_repository.get_by_id(deleted_quarentena.id)


# Testes Quarentena gato

quarentena_gato_repository = QuarentenaRepository("tests/data/quarentena/quarentena_gato_teste.json", Gato, gato_path)

quarentena_gato_id = quarentena_gato_repository.generate_id()

gato = Gato(
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
    independencia=True,
)

quarentena = Quarentena(
    id= quarentena_gato_id, animal=gato, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
)

def test_gera_id_quarentena_gato():
    assert quarentena_gato_id == quarentena.id

def test_create_quarentena_gato():
    assert quarentena_gato_repository.create(quarentena)

def test_get_all_quarentena_gato():
    quarentenas = quarentena_gato_repository.get_all()
    assert len(quarentenas) >= 1

def test_get_by_id_quarentena_gato():
    getted_quarentena = quarentena_gato_repository.get_by_id(quarentena_cacho_id)
    assert type(getted_quarentena.animal).__name__ == "Gato"

def test_update_quarentena_gato():
    getted_quarentena = quarentena_gato_repository.get_by_id(quarentena_cacho_id)

    getted_quarentena.status = "CUMPRIDA"
    getted_quarentena.data_final = datetime.now()

    quarentena_gato_repository.update(getted_quarentena)

    new_quarentena = quarentena_gato_repository.get_by_id(quarentena_cacho_id)

    assert getted_quarentena.status == new_quarentena.status

def test_delete_by_id_quarentena_gato():
    deleted_id = quarentena_gato_repository.generate_id()

    deleted_quarentena = Quarentena(
        id=deleted_id, animal=gato, data_inicial=datetime.now(), motivo="OUTRO", status="ATIVA"
    )

    quarentena_gato_repository.create(deleted_quarentena)

    quarentena_gato_repository.delete_by_id(deleted_quarentena.id)

    with pytest.raises(Exception):
        quarentena_gato_repository.get_by_id(deleted_quarentena.id)

