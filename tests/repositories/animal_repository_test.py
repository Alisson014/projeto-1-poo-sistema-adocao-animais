from src.domain import Cachorro, Calopsita, Coelho, Gato, Vacina, Evento
from src.repositories import AnimalRepository
from src.domain.exceptions import NaoCadastradoError
from datetime import datetime
from pathlib import Path

import pytest

# Garante que a pasta dos arquivos fictícios existe
Path("tests/data/animal").mkdir(parents=True, exist_ok=True)

cachorro_repository = AnimalRepository("tests/data/animal/cachorro_teste.json", Cachorro)
calopsita_repository = AnimalRepository("tests/data/animal/calopsita_teste.json", Calopsita)
coelho_repository = AnimalRepository("tests/data/animal/coelho_teste.json", Coelho)
gato_repository = AnimalRepository("tests/data/animal/gato_teste.json", Gato)

# Testes Cachorro

id_cachorro = cachorro_repository.generate_id()

vacina = Vacina(nome="vacina", data=datetime.now())
evento = Evento(tipo="VACINA", descricao="descrição", data=datetime.now())

cachorro = Cachorro(
    id=id_cachorro,
    especie="especie",
    nome="Az",
    sexo="MACHO",
    idade_meses=1,
    porte="M",
    status="DISPONIVEL",
    energia="HIPERATIVO",
    cuidado_especial=False,
    data_entrada=datetime.now(),
    historico=[evento, evento],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    vacinas=[vacina, vacina],
    raca="Golden",
    passeios_necessarios_dia=1,
)


def test_gera_id_cachorro():
    assert cachorro.id == id_cachorro


def test_create_cachorro():
    assert cachorro_repository.create(cachorro)


def test_get_all_cachorro():
    cachorros = cachorro_repository.get_all()
    assert len(cachorros) >= 1
    assert type(cachorros[id_cachorro - 1]).__name__ == "Cachorro"
    assert cachorros[id_cachorro - 1].temperamento[0].value
    assert repr(cachorro) == repr(cachorros[id_cachorro - 1])


def test_get_by_id_cachorro():
    getted_cachorro = cachorro_repository.get_by_id(id_cachorro)
    assert repr(cachorro) == repr(getted_cachorro)


def test_update_cachorro():
    getted_cachorro = cachorro_repository.get_by_id(id_cachorro)
    getted_cachorro.porte = "G"
    getted_cachorro.envelhecer()
    getted_cachorro.nome = "Ás"

    cachorro_repository.update(getted_cachorro)

    new_cachorro = cachorro_repository.get_by_id(id_cachorro)

    assert repr(new_cachorro) == repr(getted_cachorro)


def test_delete_by_id_cachorro():
    deleted_id = cachorro_repository.generate_id()

    cachorroDeleted = Cachorro(
        id=deleted_id,
        especie="especie",
        nome="Az",
        sexo="MACHO",
        idade_meses=1,
        porte="M",
        status="DISPONIVEL",
        energia="HIPERATIVO",
        cuidado_especial=False,
        data_entrada=datetime.now(),
        historico=[evento, evento],
        temperamento=["DOCIL"],
        nivel_adestramento=1,
        vacinas=[vacina, vacina],
        raca="Golden",
        passeios_necessarios_dia=1,
    )

    cachorro_repository.create(cachorroDeleted)

    cachorro_repository.delete_by_id(cachorroDeleted.id)

    with pytest.raises(NaoCadastradoError):
        cachorro_repository.get_by_id(cachorroDeleted.id)


# Testes Calopsita

id_calopsita = calopsita_repository.generate_id()

calopsita = Calopsita(
    id=id_calopsita,
    especie="especie",
    nome="Az",
    sexo="MACHO",
    idade_meses=1,
    porte="M",
    status="DISPONIVEL",
    energia="HIPERATIVO",
    cuidado_especial=False,
    data_entrada=datetime.now(),
    historico=[evento, evento],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    canta=False,
)


def test_gera_id_calopsita():
    assert calopsita.id == id_calopsita


def test_create_calopsita():
    assert calopsita_repository.create(calopsita)


def test_get_all_calopsita():
    calopsitas = calopsita_repository.get_all()
    assert len(calopsitas) >= 1
    assert type(calopsitas[id_calopsita - 1]).__name__ == "Calopsita"
    assert repr(calopsita) == repr(calopsitas[id_calopsita - 1])


def test_get_by_id_calopsita():
    getted_calopsita = calopsita_repository.get_by_id(id_calopsita)
    assert repr(calopsita) == repr(getted_calopsita)


def test_update_calopsita():
    getted_calopsita = calopsita_repository.get_by_id(id_calopsita)
    getted_calopsita.porte = "G"
    getted_calopsita.envelhecer()
    getted_calopsita.nome = "Ás"

    calopsita_repository.update(getted_calopsita)

    new_calopsita = calopsita_repository.get_by_id(id_calopsita)

    assert repr(new_calopsita) == repr(getted_calopsita)


def test_delete_by_id_calopsita():
    deleted_id = calopsita_repository.generate_id()

    calopsitaDeleted = calopsita = Calopsita(
        id=deleted_id,
        especie="especie",
        nome="Az",
        sexo="MACHO",
        idade_meses=1,
        porte="M",
        status="DISPONIVEL",
        energia="HIPERATIVO",
        cuidado_especial=False,
        data_entrada=datetime.now(),
        historico=[evento, evento],
        temperamento=["DOCIL"],
        nivel_adestramento=1,
        canta=False,
    )

    calopsita_repository.create(calopsitaDeleted)

    calopsita_repository.delete_by_id(calopsitaDeleted.id)

    with pytest.raises(NaoCadastradoError):
        calopsita_repository.get_by_id(calopsitaDeleted.id)


# Testes Coelho

id_coelho = coelho_repository.generate_id()

coelho = Coelho(
    id=id_coelho,
    especie="especie",
    nome="Az",
    sexo="MACHO",
    idade_meses=1,
    porte="M",
    status="DISPONIVEL",
    energia="HIPERATIVO",
    cuidado_especial=False,
    data_entrada=datetime.now(),
    historico=[evento, evento],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    vacinas=[vacina, vacina],
    raca="Golden",
    tamanho_gaiola_m3=1,
)


def test_gera_id_coelho():
    assert coelho.id == id_coelho


def test_create_coelho():
    assert coelho_repository.create(coelho)


def test_get_all_coelho():
    coelhos = coelho_repository.get_all()
    assert len(coelhos) >= 1
    assert type(coelhos[id_coelho - 1]).__name__ == "Coelho"
    assert coelho.id == coelhos[id_coelho - 1].id


def test_get_by_id_coelho():
    getted_coelho = coelho_repository.get_by_id(id_coelho)
    assert repr(coelho) == repr(getted_coelho)


def test_update_coelho():
    getted_coelho = coelho_repository.get_by_id(id_coelho)
    getted_coelho.porte = "G"
    getted_coelho.envelhecer()
    getted_coelho.nome = "Ás"

    coelho_repository.update(getted_coelho)

    new_coelho = coelho_repository.get_by_id(id_coelho)

    assert repr(new_coelho) == repr(getted_coelho)


def test_delete_by_id_coelho():
    deleted_id = coelho_repository.generate_id()

    coelhoDeleted = Coelho(
        id=deleted_id,
        especie="especie",
        nome="Az",
        sexo="MACHO",
        idade_meses=1,
        porte="M",
        status="DISPONIVEL",
        energia="HIPERATIVO",
        cuidado_especial=False,
        data_entrada=datetime.now(),
        historico=[evento, evento],
        temperamento=["DOCIL"],
        nivel_adestramento=1,
        vacinas=[vacina, vacina],
        raca="Golden",
        tamanho_gaiola_m3=1,
    )

    coelho_repository.create(coelhoDeleted)

    coelho_repository.delete_by_id(coelhoDeleted.id)

    with pytest.raises(NaoCadastradoError):
        coelho_repository.get_by_id(coelhoDeleted.id)


# Testes Gato

id_gato = gato_repository.generate_id()

gato = Gato(
    id=id_gato,
    especie="especie",
    nome="Az",
    sexo="MACHO",
    idade_meses=1,
    porte="M",
    status="DISPONIVEL",
    energia="HIPERATIVO",
    cuidado_especial=False,
    data_entrada=datetime.now(),
    historico=[evento, evento],
    temperamento=["DOCIL"],
    nivel_adestramento=1,
    vacinas=[vacina, vacina],
    raca="Golden",
    independencia=True,
)


def test_gera_id_gato():
    assert gato.id == id_gato


def test_create_gato():
    assert gato_repository.create(gato)


def test_get_all_gato():
    gatos = gato_repository.get_all()
    assert len(gatos) >= 1
    assert type(gatos[id_gato - 1]).__name__ == "Gato"
    assert gato.id == gatos[id_gato - 1].id


def test_get_by_id_gato():
    getted_gato = gato_repository.get_by_id(id_gato)
    assert repr(gato) == repr(getted_gato)


def test_update_gato():
    getted_gato = gato_repository.get_by_id(id_gato)
    getted_gato.porte = "G"
    getted_gato.envelhecer()
    getted_gato.nome = "Ás"

    gato_repository.update(getted_gato)

    new_gato = gato_repository.get_by_id(id_gato)

    assert repr(new_gato) == repr(getted_gato)


def test_delete_by_id_gato():
    deleted_id = gato_repository.generate_id()

    gatoDeleted = Gato(
        id=deleted_id,
        especie="especie",
        nome="Az",
        sexo="MACHO",
        idade_meses=1,
        porte="M",
        status="DISPONIVEL",
        energia="HIPERATIVO",
        cuidado_especial=False,
        data_entrada=datetime.now(),
        historico=[evento, evento],
        temperamento=["DOCIL"],
        nivel_adestramento=1,
        vacinas=[vacina, vacina],
        raca="Golden",
        independencia=True,
    )

    gato_repository.create(gatoDeleted)

    gato_repository.delete_by_id(gatoDeleted.id)

    with pytest.raises(NaoCadastradoError):
        gato_repository.get_by_id(gatoDeleted.id)
