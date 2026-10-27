# Declaro utilização de IA para a revisão de código e geração dos testes unitários abaixo
# IA utilizada: claude
# prompt:
"""
Disponível no arquivo de service referente a este domínio
"""

from src.domain import Cachorro, Adotante, Adocao, Devolucao
from src.services import TaxaDevolucoesService
from src.domain.exceptions import NaoCadastradoError

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

adotante = Adotante(
    nome="Maria",
    email="maria@email.com",
    idade=30,
    moradia="CASA_COM_QUINTAL",
    experiencia="INICIANTE",
    tempo_livre_min=120,
    possui_criancas=False,
    outros_animais=False,
    area_util=80.0,
)

def nova_adocao(id: int) -> Adocao:
    return Adocao(
        id=id,
        animal=novo_cachorro(id),
        adotante=adotante,
        taxa=100.0,
        pago=True,
        data=datetime(2025, 2, 10),
    )

def nova_devolucao(id: int) -> Devolucao:
    return Devolucao(
        id=id,
        animal=novo_cachorro(id),
        adotante=adotante,
        motivo="COMPORTAMENTO",
        data=datetime(2025, 3, 10),
    )

def novo_relatorio_data() -> dict:
    # 1 devolução para 2 adoções -> taxa de 50%
    return {
        "data": datetime(2025, 4, 1),
        "nome": "Relatório de taxa de devoluções",
        "adocoes": [nova_adocao(1), nova_adocao(2)],
        "devolucoes": [nova_devolucao(1)],
    }

relatorio_service = TaxaDevolucoesService("tests/data/relatorio/taxa_devolucoes_teste.json")


def setup_module():
    # Garante um banco limpo mesmo que uma execução anterior tenha sido interrompida
    relatorio_service.delete_all()


def test_create():
    relatorio = relatorio_service.create(novo_relatorio_data())

    assert type(relatorio).__name__ == "TaxaDevolucoes"
    assert relatorio.id == 1
    assert relatorio.taxa == "50.00%"

def test_get_all():
    relatorios = relatorio_service.get_all()

    assert len(relatorios) >= 1
    assert type(relatorios[0]).__name__ == "TaxaDevolucoes"

def test_get_by_id():
    relatorio = relatorio_service.get_by_id(1)

    assert type(relatorio).__name__ == "TaxaDevolucoes"
    assert len(relatorio.adocoes) == 2
    assert len(relatorio.devolucoes) == 1
    assert type(relatorio.devolucoes[0]).__name__ == "Devolucao"
    assert relatorio.taxa == "50.00%"

def test_get_by_id_error_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        relatorio_service.get_by_id(9999)

def test_update():
    updated_relatorio_data = {
        "nome": "Nome atualizado",
        "devolucoes": [nova_devolucao(1), nova_devolucao(2)],
    }

    res = relatorio_service.update(updated_relatorio_data, 1)

    assert type(res).__name__ == "TaxaDevolucoes"
    assert res.nome == "Nome atualizado"
    assert len(res.devolucoes) == 2
    # A taxa é recalculada: 2 devoluções para 2 adoções
    assert res.taxa == "100.00%"

    # Verifica a persistência da atualização
    persistido = relatorio_service.get_by_id(1)
    assert len(persistido.devolucoes) == 2
    assert persistido.taxa == "100.00%"

def test_update_ignora_id():
    res = relatorio_service.update({"id": 9999}, 1)

    assert res.id == 1

def test_update_error_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        relatorio_service.update({"nome": "novo"}, 9999)

def test_delete_by_id():
    relatorio = relatorio_service.create(novo_relatorio_data())

    relatorio_service.delete_by_id(relatorio.id)

    with pytest.raises(NaoCadastradoError):
        relatorio_service.get_by_id(relatorio.id)

def test_delete_by_id_error_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        relatorio_service.delete_by_id(9999)

# Será utilizado apenas na versão final da aplciação
# Deve ser o último teste do arquivo, pois limpa o banco de dados
# def test_delete_all():
#     relatorio_service.delete_all()

#     assert relatorio_service.get_all() == []

#     with pytest.raises(NaoCadastradoError):
#         relatorio_service.get_by_id(1)
