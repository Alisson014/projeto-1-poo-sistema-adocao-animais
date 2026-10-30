# Declaro utilização de IA para a revisão de código e geração dos testes unitários abaixo
# IA utilizada: claude
# prompt:
"""
Disponível no arquivo de service referente a este domínio
"""

from src.domain import Cachorro, Adotante
from src.services import Top5MaisAdotaveisService
from src.domain.exceptions import NaoCadastradoError, RelatorioNaoGeradoError

from src.config import PesosCompatibilidade
from src.repositories import PoliticaRepository

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

def novo_relatorio_data(qtd_animais: int = 2) -> dict:
    return {
        "data": datetime(2025, 3, 1),
        "nome": "Top 5 mais adotáveis",
        "animais": [novo_cachorro(i) for i in range(1, qtd_animais + 1)],
        "adotantes": [adotante],
    }

relatorio_service = Top5MaisAdotaveisService("tests/data/relatorio/top5_mais_adotaveis_teste.json", "tests/data/settings.json")


def setup_module():
    # Garante um banco limpo mesmo que uma execução anterior tenha sido interrompida
    relatorio_service.delete_all()


def test_create():
    relatorio = relatorio_service.create(novo_relatorio_data())

    assert type(relatorio).__name__ == "Top5MaisAdotaveis"
    assert relatorio.id == 1
    assert len(relatorio.top5) == 2

def test_create_top5_nao_compartilha_estado():
    relatorio_1 = relatorio_service.create(novo_relatorio_data())
    relatorio_2 = relatorio_service.create(novo_relatorio_data())

    assert len(relatorio_1.top5) == 2
    assert len(relatorio_2.top5) == 2

    relatorio_service.delete_by_id(relatorio_1.id)
    relatorio_service.delete_by_id(relatorio_2.id)

def test_create_limita_top5_em_cinco():
    relatorio = relatorio_service.create(novo_relatorio_data(qtd_animais=7))

    assert len(relatorio.animais) == 7
    assert len(relatorio.top5) == 5

    relatorio_service.delete_by_id(relatorio.id)

def test_get_all():
    relatorios = relatorio_service.get_all()

    assert len(relatorios) >= 1
    assert type(relatorios[0]).__name__ == "Top5MaisAdotaveis"

def test_get_by_id():
    relatorio = relatorio_service.get_by_id(1)

    assert type(relatorio).__name__ == "Top5MaisAdotaveis"
    assert len(relatorio.animais) == 2
    assert len(relatorio.adotantes) == 1
    assert len(relatorio.top5) == 2

def test_get_by_id_error_nao_cadastrado():
    with pytest.raises(NaoCadastradoError):
        relatorio_service.get_by_id(9999)

def test_update():
    updated_relatorio_data = {
        "nome": "Nome atualizado",
        "animais": [novo_cachorro(1), novo_cachorro(2), novo_cachorro(3)],
    }

    res = relatorio_service.update(updated_relatorio_data, 1)

    assert type(res).__name__ == "Top5MaisAdotaveis"
    assert res.nome == "Nome atualizado"
    assert len(res.animais) == 3
    # O top5 é recalculado, sem duplicar os animais do cálculo anterior
    assert len(res.top5) == 3

    # Verifica a persistência da atualização
    persistido = relatorio_service.get_by_id(1)
    assert len(persistido.animais) == 3
    assert len(persistido.top5) == 3

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

# Será utilizado apenas na versão final da aplicação
# Deve ser o último teste do arquivo, pois limpa o banco de dados
# def test_delete_all():
#     relatorio_service.delete_all()

#     assert relatorio_service.get_all() == []

#     # Banco vazio: get_by_id também deve lançar a exceção
#     with pytest.raises(NaoCadastradoError):
#         relatorio_service.get_by_id(1)
