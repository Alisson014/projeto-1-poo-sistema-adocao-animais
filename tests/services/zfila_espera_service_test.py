# Declaro utilização de IA para a revisão de código e geração dos testes unitários abaixo
# IA utilizada: claude
# prompt:
"""
Disponível no arquivo de service referente a este domínio
"""

from src.domain import Cachorro, Adotante
from src.services import FilaEsperaService
from src.domain.exceptions import NaoCadastradoError, NaoEncontradoError

from datetime import datetime
import pytest


# Dados auxiliares
def novo_cachorro(id: int) -> Cachorro:
    return Cachorro(
        id=id,
        especie="especie",
        nome=f"Az{id}",
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

def novo_adotante(n: int) -> Adotante:
    return Adotante(
        nome=f"Adotante {n}",
        email=f"adotante{n}@email.com",
        idade=30,
        moradia="CASA_COM_QUINTAL",
        experiencia="INICIANTE",
        tempo_livre_min=120,
        possui_criancas=False,
        outros_animais=False,
        area_util=80.0,
    )

fila_service = FilaEsperaService(
    "tests/data/fila_espera/fila_cachorro_teste.json",
    Cachorro,
    "tests/data/fila_espera/cachorro_teste.json",
    "tests/data/fila_espera/adotante_teste.json",
)


def setup_module():
    # Garante um banco limpo mesmo que uma execução anterior tenha sido interrompida
    fila_service.delete_all()
    fila_service.animal_repository.delete_all(True)
    fila_service.adotante_repository.delete_all(True)

    # A fila de espera depende de animais e adotantes cadastrados
    for i in range(1, 4):
        fila_service.animal_repository.create(novo_cachorro(i))
        fila_service.adotante_repository.create(novo_adotante(i))


def test_create():
    fila = fila_service.create(1)

    assert type(fila).__name__ == "FilaEspera"
    assert fila.animal.id == 1
    assert len(fila) == 0

def test_create_error_animal_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        fila_service.create(9999)

def test_create_error_fila_duplicada():
    with pytest.raises(Exception, match="já possui uma fila de espera"):
        fila_service.create(1)

def test_get_all():
    filas = fila_service.get_all()

    assert len(filas) >= 1
    assert type(filas[0]).__name__ == "FilaEspera"

def test_get_by_animal_id():
    fila = fila_service.get_by_animal_id(1)

    assert type(fila).__name__ == "FilaEspera"
    assert fila.animal.id == 1

def test_get_by_animal_id_error_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        fila_service.get_by_animal_id(9999)

def test_add_adotante():
    fila = fila_service.add_adotante(1, "adotante1@email.com")

    assert len(fila) == 1

    # Verifica a persistência da atualização
    assert len(fila_service.get_by_animal_id(1)) == 1

def test_add_adotante_segundo_adotante():
    fila = fila_service.add_adotante(1, "adotante2@email.com")

    assert len(fila) == 2
    assert len(fila_service.get_by_animal_id(1)) == 2

def test_add_adotante_error_duplicado():
    with pytest.raises(Exception, match="mesma fila duas vezes"):
        fila_service.add_adotante(1, "adotante1@email.com")

def test_add_adotante_error_adotante_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        fila_service.add_adotante(1, "naoexiste@email.com")

def test_add_adotante_error_fila_nao_cadastrada():
    with pytest.raises(NaoCadastradoError):
        fila_service.add_adotante(9999, "adotante1@email.com")

def test_proximo():
    entrada = fila_service.proximo(1)

    assert type(entrada).__name__ == "EntradaFila"
    assert entrada.adotante.email == "adotante1@email.com"

def test_proximo_fila_vazia():
    fila_service.create(2)

    assert fila_service.proximo(2) is None

def test_proximo_error_fila_nao_cadastrada():
    with pytest.raises(NaoCadastradoError):
        fila_service.proximo(9999)

def test_remove_adotante():
    fila = fila_service.remove_adotante(1, "adotante1@email.com")

    assert len(fila) == 1
    assert fila_service.proximo(1).adotante.email == "adotante2@email.com"

    # Verifica a persistência da atualização
    assert len(fila_service.get_by_animal_id(1)) == 1

def test_remove_adotante_error_nao_encontrado():
    # O adotante 3 está cadastrado, mas não está na fila
    with pytest.raises(NaoEncontradoError):
        fila_service.remove_adotante(1, "adotante3@email.com")

def test_remove_adotante_error_adotante_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        fila_service.remove_adotante(1, "naoexiste@email.com")

def test_get_by_animal_id_limpa_adotantes_removidos():
    fila_service.add_adotante(1, "adotante3@email.com")
    assert len(fila_service.get_by_animal_id(1)) == 2

    # Remove o adotante do banco: a entrada deve ser descartada da fila
    fila_service.adotante_repository.delete_by_email("adotante3@email.com")

    fila = fila_service.get_by_animal_id(1)
    assert len(fila) == 1
    assert fila_service.proximo(1).adotante.email == "adotante2@email.com"

def test_get_by_animal_id_remove_fila_de_animal_inexistente():
    # A fila do animal 2 existe, mas o animal é removido do banco
    fila_service.animal_repository.delete_by_id(2)

    with pytest.raises(NaoCadastradoError):
        fila_service.get_by_animal_id(2)

    # A fila foi removida por integridade, então não existe mais
    with pytest.raises(NaoCadastradoError):
        fila_service.delete_by_animal_id(2)

"""Necessita de revisão"""
# def test_get_all_ignora_filas_invalidas():
#     fila_service.create(3)

#     # A fila do animal 1 passa a ser inválida, mas a do animal 3 deve continuar sendo retornada
#     fila_service.animal_repository.delete_by_id(1)

#     filas = fila_service.get_all()

#     assert len(filas) == 1
#     assert filas[0].animal.id == 3

def test_delete_by_animal_id():
    fila_service.create(3)
    fila_service.delete_by_animal_id(3)

    with pytest.raises(NaoCadastradoError):
        fila_service.get_by_animal_id(3)

def test_delete_by_animal_id_error_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        fila_service.delete_by_animal_id(9999)

# Será utilizado apenas na versão final da aplicação
# Deve ser o último teste do arquivo, pois limpa o banco de dados
# def test_delete_all():
#     fila_service.delete_all()

#     assert fila_service.get_all() == []

#     with pytest.raises(NaoCadastradoError):
#         fila_service.get_by_animal_id(3)