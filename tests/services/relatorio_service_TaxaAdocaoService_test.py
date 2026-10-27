# Declaro utilização de IA para a revisão de código e geração dos testes unitários abaixo
# IA utilizada: claude
# prompt:
"""
Disponível no arquivo de service referente a este domínio
"""

from src.domain import Cachorro, Adotante, Adocao
from src.domain import TaxaAdocaoPorte, TaxaAdocaoEspecies, TaxaTempoMedioEntradaAdocao
from src.services import TaxaAdocaoService
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
    # Entrada do animal em 10/01/2025 -> adoção de 1 mês
    return Adocao(
        id=id,
        animal=novo_cachorro(id),
        adotante=adotante,
        taxa=100.0,
        pago=True,
        data=datetime(2025, 2, 10),
    )

def novo_relatorio_data(qtd_adocoes: int = 2) -> dict:
    return {
        "data": datetime(2025, 3, 1),
        "nome": "Relatório de taxa de adoção",
        "adocoes": [nova_adocao(i) for i in range(1, qtd_adocoes + 1)],
    }

# Um service (e um arquivo json) para cada subclasse de relatório
services = {
    "TaxaAdocaoPorte": TaxaAdocaoService("tests/data/relatorio/taxa_adocao_porte_teste.json", TaxaAdocaoPorte),
    "TaxaAdocaoEspecies": TaxaAdocaoService("tests/data/relatorio/taxa_adocao_especies_teste.json", TaxaAdocaoEspecies),
    "TaxaTempoMedioEntradaAdocao": TaxaAdocaoService("tests/data/relatorio/taxa_tempo_medio_entrada_adocao_teste.json", TaxaTempoMedioEntradaAdocao),
}

# Verificação do resultado de gerar() para 2 adoções de cachorros de porte M, com 1 mês entre entrada e adoção
resultados_gerados = {
    "TaxaAdocaoPorte": lambda r: r.taxas["M"] == "2/2",
    "TaxaAdocaoEspecies": lambda r: r.taxas["Cachorro"] == "2/2",
    "TaxaTempoMedioEntradaAdocao": lambda r: r.tempo_medio_meses == 1,
}

tipos = pytest.mark.parametrize("tipo", list(services.keys()))


def setup_module():
    # Garante um banco limpo mesmo que uma execução anterior tenha sido interrompida
    for service in services.values():
        service.delete_all()


@tipos
def test_create(tipo):
    relatorio = services[tipo].create(novo_relatorio_data())

    assert type(relatorio).__name__ == tipo
    assert relatorio.id == 1
    assert resultados_gerados[tipo](relatorio)

@tipos
def test_get_all(tipo):
    relatorios = services[tipo].get_all()

    assert len(relatorios) >= 1
    assert type(relatorios[0]).__name__ == tipo

@tipos
def test_get_by_id(tipo):
    relatorio = services[tipo].get_by_id(1)

    assert type(relatorio).__name__ == tipo
    assert len(relatorio.adocoes) == 2
    assert type(relatorio.adocoes[0]).__name__ == "Adocao"
    assert resultados_gerados[tipo](relatorio)

@tipos
def test_get_by_id_error_nao_cadastrado(tipo):
    with pytest.raises(NaoCadastradoError):
        services[tipo].get_by_id(9999)

@tipos
def test_update(tipo):
    updated_relatorio_data = {
        "nome": "Nome atualizado",
        "adocoes": [nova_adocao(1), nova_adocao(2), nova_adocao(3)],
    }

    res = services[tipo].update(updated_relatorio_data, 1)

    assert type(res).__name__ == tipo
    assert res.nome == "Nome atualizado"
    assert len(res.adocoes) == 3

    # Verifica a persistência da atualização
    assert len(services[tipo].get_by_id(1).adocoes) == 3

@tipos
def test_update_ignora_id(tipo):
    res = services[tipo].update({"id": 9999}, 1)

    assert res.id == 1

@tipos
def test_update_error_nao_cadastrado(tipo):
    with pytest.raises(NaoCadastradoError):
        services[tipo].update({"nome": "novo"}, 9999)

@tipos
def test_delete_by_id(tipo):
    relatorio = services[tipo].create(novo_relatorio_data())

    services[tipo].delete_by_id(relatorio.id)

    with pytest.raises(NaoCadastradoError):
        services[tipo].get_by_id(relatorio.id)

@tipos
def test_delete_by_id_error_nao_cadastrado(tipo):
    with pytest.raises(NaoCadastradoError):
        services[tipo].delete_by_id(9999)

# Será utilizado apenas na versão final da aplicação
# Deve ser o último teste do arquivo, pois limpa o banco de dados
# @tipos
# def test_delete_all(tipo):
#     services[tipo].delete_all()

#     assert services[tipo].get_all() == []

#     with pytest.raises(NaoCadastradoError):
#         services[tipo].get_by_id(1)