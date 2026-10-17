from src.domain import Adotante, Cachorro, Animal, Adocao, Devolucao, Reserva
from src.domain.models import Quarentena
from src.repositories import RegistroRepository, PessoaRespository
from src.domain.exceptions import NaoCadastradoError

from random import randint
from datetime import datetime
import pytest

cachorro_path = "tests/data/animal/cachorro_teste.json"
calopsita_path = "tests/data/animal/calopsita_teste.json"
coelho_path = "tests/data/animal/coelho_teste.json"
gato_path = "tests/data/animal/gato_teste.json"
adotante_path = "tests/data/pessoa/adotante_teste.json"

adocao_path = "tests/data/registro/adocao_teste.json"
devolucao_path = "tests/data/registro/devolucao_teste.json"
reserva_path = "tests/data/registro/reserva_teste.json"

adocao_repository = RegistroRepository(adocao_path, Adocao, cachorro_path, Cachorro, adotante_path)
devolucao_repository = RegistroRepository(devolucao_path, Devolucao, cachorro_path, Cachorro, adotante_path)
reserva_repository = RegistroRepository(reserva_path, Reserva, cachorro_path, Cachorro, adotante_path)


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

PessoaRespository(adotante_path, Adotante).create(adotante)
adotante = PessoaRespository(adotante_path, Adotante).get_by_email(email) # type: ignore[arg-type]

# Testes Registro Adocao

adocao_id = adocao_repository.generate_id()

adocao = Adocao(
    id=adocao_id,
    animal=cachorro,
    adotante=adotante,
    taxa=10,
    pago=False,
    data=datetime.now(),
)

def test_generate_id_adocao():
    assert adocao.id == adocao_id

def test_create_adocao():
    assert adocao_repository.create(adocao)

def test_get_all_adocao():
    adocoes = adocao_repository.get_all()
    assert len(adocoes) >= 1

def test_get_by_id_adocao():
    getted_adocao = adocao_repository.get_by_id(adocao_id)
    assert type(getted_adocao.animal).__name__ == "Cachorro"

def test_update_adocao():
    getted_adocao = adocao_repository.get_by_id(adocao_id)

    getted_adocao.pago = True

    adocao_repository.update(getted_adocao)

    new_adocao = adocao_repository.get_by_id(adocao_id)

    assert new_adocao.pago == getted_adocao.pago

def test_delete_by_id():
    deleted_id = adocao_repository.generate_id()
    deleted_adocao = Adocao(
        id=deleted_id,
        animal=cachorro,
        adotante=adotante,
        taxa=10,
        pago=False,
        data=datetime.now(),
    )

    adocao_repository.create(deleted_adocao)

    adocao_repository.delete_by_id(deleted_id)

    with pytest.raises(NaoCadastradoError):
        adocao_repository.get_by_id(deleted_id)


# Testes Registro Devolucoes

devolucao_id = devolucao_repository.generate_id()

devolucao = Devolucao(
    id=devolucao_id, animal=cachorro, adotante=adotante, motivo="OUTRO", data=datetime.now()
)

def test_generate_id_devolucao():
    assert devolucao.id == devolucao_id

def test_create_devolucao():
    assert devolucao_repository.create(devolucao)

def test_get_all_devolucao():
    devolucoes = devolucao_repository.get_all()
    assert len(devolucoes) >= 1

def test_get_by_id_devolucao():
    getted_devolucao = devolucao_repository.get_by_id(devolucao_id)
    assert type(getted_devolucao.animal).__name__ == "Cachorro"

def test_update_devolucao():
    getted_devolucao = devolucao_repository.get_by_id(devolucao_id)

    getted_devolucao.motivo = "PESSOAL"

    devolucao_repository.update(getted_devolucao)

    new_devolucao = devolucao_repository.get_by_id(devolucao_id)

    assert new_devolucao.motivo == getted_devolucao.motivo

def test_delete_by_id_devolucao():
    deleted_id = devolucao_repository.generate_id()
    deleted_devolucao = Devolucao(
        id=deleted_id, animal=cachorro, adotante=adotante, motivo="OUTRO", data=datetime.now()
    )

    devolucao_repository.create(deleted_devolucao)

    devolucao_repository.delete_by_id(deleted_id)

    with pytest.raises(NaoCadastradoError):
        devolucao_repository.get_by_id(deleted_id)


# Testes Registro Reserva

reserva_id = reserva_repository.generate_id()

reserva = Reserva(
    id=reserva_id,
    animal=cachorro,
    adotante=adotante,
    data_inicial=datetime.now(),
    data_expiracao=datetime.now(),
    status="ATIVA",
    compatibilidade=100,
)

def test_generate_id_reserva():
    assert reserva.id == reserva_id

def test_create_reserva():
    assert reserva_repository.create(reserva)

def test_get_all_reserva():
    devolucoes = reserva_repository.get_all()
    assert len(devolucoes) >= 1

def test_get_by_id_reserva():
    getted_reserva = reserva_repository.get_by_id(reserva_id)
    assert type(getted_reserva.animal).__name__ == "Cachorro"

def test_update_reserva():
    getted_reserva = reserva_repository.get_by_id(reserva_id)

    getted_reserva.compatibilidade = 95

    reserva_repository.update(getted_reserva)

    new_reserva = reserva_repository.get_by_id(reserva_id)

    assert new_reserva.compatibilidade == getted_reserva.compatibilidade

def test_delete_by_id_reserva():
    deleted_id = reserva_repository.generate_id()
    
    deleted_reserva = Reserva(
        id=deleted_id,
        animal=cachorro,
        adotante=adotante,
        data_inicial=datetime.now(),
        data_expiracao=datetime.now(),
        status="ATIVA",
        compatibilidade=100,
    )

    reserva_repository.create(deleted_reserva)

    reserva_repository.delete_by_id(deleted_id)

    with pytest.raises(NaoCadastradoError):
        reserva_repository.get_by_id(deleted_id)