# Declaro utilização de IA para a revisão de código e geração dos testes unitários abaixo
# IA utilizada: claude
# prompt:
"""
Estou desenvolvendo um projeto em python de um sistema de gerenciamente de adoção 
de animais em python para praticar conceitos em poo. O projeto utiliza o padrão repository
para a persistência dos dados (armazenados em json).

No momento, estou finalizando o último repository dentro do sistema e preciso 
criar testes unitários para validar o código produzido. Os testes unitários do sistema 
são codificados em pytest, sendo que arquivos json fictícios são criados 
simulando o funcionamento do projeto no contexto da produção.

Abaixo, deixo a base do caminho que você deve 
utilizar para o atributo path das Classes Repository:
tests/data/relatorio/nome_do_relatorio.json

É importante que cada tipo de relatório tenha um arquivo 
json único para armazenar seus dados.

Em anexo, enviarei:

1. O código das classes repository;
2. As classes que modelam os relatórios;
3. Um arquivo com testes unitários de outro repository;


É importante que você utilize 'registro_repository_test.py' como base para a 
criação dos testes unitários de Relatório_Repository. Você deve seguir o mesmo 
padrão para garantir consistência do padrão de código do sistema.

Sua tarefa deve ter as seguintes saídas:

* O código com os testes unitários para o domínio de relatórios;
* Apontamentos de erros graves no código do repository que comprometam o sistema.


Um dado importânte sobre o sistema, 
o fato de classes externas (como Adocao, Devolucao, etc) estarem 
sendo armazenadas inteiramente e não por referência não é um erro. 
A ideia dos relatórios é que eles representem um estado específico do sistema, 
o que não aconteceria se os dados fossem armazenados por referência.
"""

from src.domain import (
    Adotante,
    Cachorro,
    Adocao,
    Devolucao,
    Top5MaisAdotaveis,
    TaxaAdocaoEspecies,
    TaxaAdocaoPorte,
    TaxaTempoMedioEntradaAdocao,
    TaxaDevolucoes,
)
from src.repositories import (
    PessoaRespository,
    Top5MaisAdotaveisRepository,
    TaxaAdocaoRepository,
    TaxaDevolucoesRepository,
)
from src.domain.exceptions import NaoCadastradoError

from random import randint
from datetime import datetime
from pathlib import Path
import pytest

adotante_path = "tests/data/pessoa/adotante_teste.json"

top5_path = "tests/data/relatorio/top5_mais_adotaveis_teste.json"
taxa_especies_path = "tests/data/relatorio/taxa_adocao_especies_teste.json"
taxa_porte_path = "tests/data/relatorio/taxa_adocao_porte_teste.json"
taxa_tempo_medio_path = "tests/data/relatorio/taxa_tempo_medio_entrada_adocao_teste.json"
taxa_devolucoes_path = "tests/data/relatorio/taxa_devolucoes_teste.json"

# Garante que a pasta dos arquivos fictícios existe
Path("tests/data/relatorio").mkdir(parents=True, exist_ok=True)

top5_repository = Top5MaisAdotaveisRepository(top5_path)
taxa_especies_repository = TaxaAdocaoRepository(taxa_especies_path, TaxaAdocaoEspecies)
taxa_porte_repository = TaxaAdocaoRepository(taxa_porte_path, TaxaAdocaoPorte)
taxa_tempo_medio_repository = TaxaAdocaoRepository(
    taxa_tempo_medio_path, TaxaTempoMedioEntradaAdocao
)
taxa_devolucoes_repository = TaxaDevolucoesRepository(taxa_devolucoes_path)


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
    # Entrada no passado para que o tempo médio até a adoção seja > 0 meses
    data_entrada=datetime(2025, 1, 10),
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
adotante = PessoaRespository(adotante_path, Adotante).get_by_email(email)  # type: ignore[arg-type]


# Funções auxiliares para criar instâncias novas.
# Os repositories podem alterar o objeto recebido, então instâncias
# novas evitam que um teste interfira no outro.

def criar_adocao(id=1):
    return Adocao(
        id=id,
        animal=cachorro,
        adotante=adotante,
        taxa=10,
        pago=False,
        data=datetime.now(),
    )

def criar_devolucao(id=1):
    return Devolucao(
        id=id,
        animal=cachorro,
        adotante=adotante,
        motivo="OUTRO",
        data=datetime.now(),
    )

def criar_top5(id):
    return Top5MaisAdotaveis(
        id=id,
        data=datetime.now(),
        nome="Top 5 teste",
        animais=[cachorro],
        adotantes=[adotante],
    )

def criar_taxa_especies(id):
    return TaxaAdocaoEspecies(
        id=id, data=datetime.now(), nome="Taxa especies teste", adocoes=[criar_adocao()]
    )

def criar_taxa_porte(id):
    return TaxaAdocaoPorte(
        id=id, data=datetime.now(), nome="Taxa porte teste", adocoes=[criar_adocao()]
    )

def criar_taxa_tempo_medio(id):
    return TaxaTempoMedioEntradaAdocao(
        id=id, data=datetime.now(), nome="Tempo medio teste", adocoes=[criar_adocao()]
    )

def criar_taxa_devolucoes(id):
    return TaxaDevolucoes(
        id=id,
        data=datetime.now(),
        nome="Taxa devolucoes teste",
        adocoes=[criar_adocao()],
        devolucoes=[criar_devolucao()],
    )


# Testes Relatorio Top5MaisAdotaveis

top5_id = top5_repository.generate_id()

top5 = criar_top5(top5_id)

def test_generate_id_top5():
    assert top5.id == top5_id

def test_create_top5():
    assert top5_repository.create(top5)

def test_create_duplicado_top5():
    with pytest.raises(Exception, match="já cadastrad"):
        top5_repository.create(criar_top5(top5_id))

def test_get_all_top5():
    relatorios = top5_repository.get_all()
    assert len(relatorios) >= 1

def test_get_by_id_top5():
    getted_top5 = top5_repository.get_by_id(top5_id)

    assert isinstance(getted_top5, Top5MaisAdotaveis)
    assert getted_top5.id == top5_id
    assert type(getted_top5.animais[0]).__name__ == "Cachorro"
    assert type(getted_top5.adotantes[0]).__name__ == "Adotante"
    # Só há um animal cadastrado, então o top5 tem apenas um
    assert len(getted_top5.top5) == 1
    assert type(getted_top5.top5[0]).__name__ == "Cachorro"

def test_get_by_id_inexistente_top5():
    with pytest.raises(NaoCadastradoError):
        top5_repository.get_by_id(top5_repository.generate_id())

def test_update_top5():
    getted_top5 = top5_repository.get_by_id(top5_id)

    getted_top5.nome = "Top 5 atualizado"

    top5_repository.update(getted_top5)

    new_top5 = top5_repository.get_by_id(top5_id)

    assert new_top5.nome == getted_top5.nome

def test_update_inexistente_top5():
    with pytest.raises(NaoCadastradoError):
        top5_repository.update(criar_top5(top5_repository.generate_id()))

def test_delete_by_id_top5():
    deleted_id = top5_repository.generate_id()

    top5_repository.create(criar_top5(deleted_id))

    top5_repository.delete_by_id(deleted_id)

    with pytest.raises(NaoCadastradoError):
        top5_repository.get_by_id(deleted_id)

def test_delete_by_id_inexistente_top5():
    with pytest.raises(NaoCadastradoError):
        top5_repository.delete_by_id(top5_repository.generate_id())


# Testes Relatorio TaxaAdocao (Especies, Porte e TempoMedioEntradaAdocao)
# Os três tipos compartilham o mesmo repository, cada um com seu arquivo json.

CASOS_TAXA_ADOCAO = {
    "especies": (taxa_especies_repository, criar_taxa_especies, TaxaAdocaoEspecies),
    "porte": (taxa_porte_repository, criar_taxa_porte, TaxaAdocaoPorte),
    "tempo_medio": (
        taxa_tempo_medio_repository,
        criar_taxa_tempo_medio,
        TaxaTempoMedioEntradaAdocao,
    ),
}

taxa_ids = {
    nome: repository.generate_id()
    for nome, (repository, _, _) in CASOS_TAXA_ADOCAO.items()
}

taxa_relatorios = {
    nome: criar(taxa_ids[nome])
    for nome, (_, criar, _) in CASOS_TAXA_ADOCAO.items()
}

def criar_e_salvar_taxa(nome, id):
    repository, criar, _ = CASOS_TAXA_ADOCAO[nome]
    relatorio = criar(id)
    repository.create(relatorio)
    return relatorio

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_generate_id_taxa_adocao(nome):
    assert taxa_relatorios[nome].id == taxa_ids[nome]

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_create_taxa_adocao(nome):
    repository, _, _ = CASOS_TAXA_ADOCAO[nome]
    relatorio = taxa_relatorios[nome]

    assert repository.create(relatorio)

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_create_gera_relatorio_taxa_adocao(nome):
    repository, criar, classe = CASOS_TAXA_ADOCAO[nome]
    novo_id = repository.generate_id()

    assert repository.create(criar(novo_id))

    getted_relatorio = repository.get_by_id(novo_id)
    assert isinstance(getted_relatorio, classe)

    repository.delete_by_id(novo_id)

def test_create_gera_relatorio_taxa_devolucoes():
    novo_id = taxa_devolucoes_repository.generate_id()

    assert taxa_devolucoes_repository.create(criar_taxa_devolucoes(novo_id))

    assert taxa_devolucoes_repository.get_by_id(novo_id).taxa == "100.00%"

    taxa_devolucoes_repository.delete_by_id(novo_id)

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_create_duplicado_taxa_adocao(nome):
    repository, criar, _ = CASOS_TAXA_ADOCAO[nome]
    duplicado = criar(taxa_ids[nome])

    with pytest.raises(Exception, match="já cadastrad"):
        repository.create(duplicado)

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_get_all_taxa_adocao(nome):
    repository, _, _ = CASOS_TAXA_ADOCAO[nome]
    relatorios = repository.get_all()
    assert len(relatorios) >= 1

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_get_by_id_taxa_adocao(nome):
    repository, _, classe = CASOS_TAXA_ADOCAO[nome]

    getted_relatorio = repository.get_by_id(taxa_ids[nome])

    assert isinstance(getted_relatorio, classe)
    assert getted_relatorio.id == taxa_ids[nome]
    assert len(getted_relatorio.adocoes) == 1
    assert type(getted_relatorio.adocoes[0].animal).__name__ == "Cachorro"
    assert type(getted_relatorio.adocoes[0].adotante).__name__ == "Adotante"

def test_get_by_id_preserva_taxas_especies():
    getted_relatorio = taxa_especies_repository.get_by_id(taxa_ids["especies"])
    assert getted_relatorio.taxas == taxa_relatorios["especies"].taxas

def test_get_by_id_preserva_taxas_porte():
    getted_relatorio = taxa_porte_repository.get_by_id(taxa_ids["porte"])
    assert getted_relatorio.taxas == taxa_relatorios["porte"].taxas

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_get_by_id_inexistente_taxa_adocao(nome):
    repository, _, _ = CASOS_TAXA_ADOCAO[nome]

    with pytest.raises(NaoCadastradoError):
        repository.get_by_id(repository.generate_id())

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_update_taxa_adocao(nome):
    repository, _, _ = CASOS_TAXA_ADOCAO[nome]

    getted_relatorio = repository.get_by_id(taxa_ids[nome])

    getted_relatorio.nome = "Nome atualizado"

    repository.update(getted_relatorio)

    new_relatorio = repository.get_by_id(taxa_ids[nome])

    assert new_relatorio.nome == getted_relatorio.nome

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_update_inexistente_taxa_adocao(nome):
    repository, criar, _ = CASOS_TAXA_ADOCAO[nome]
    inexistente = criar(repository.generate_id())

    with pytest.raises(NaoCadastradoError):
        repository.update(inexistente)

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_delete_by_id_taxa_adocao(nome):
    repository, _, _ = CASOS_TAXA_ADOCAO[nome]
    deleted_id = repository.generate_id()

    criar_e_salvar_taxa(nome, deleted_id)

    repository.delete_by_id(deleted_id)

    with pytest.raises(NaoCadastradoError):
        repository.get_by_id(deleted_id)

@pytest.mark.parametrize("nome", list(CASOS_TAXA_ADOCAO))
def test_delete_by_id_inexistente_taxa_adocao(nome):
    repository, _, _ = CASOS_TAXA_ADOCAO[nome]

    with pytest.raises(NaoCadastradoError):
        repository.delete_by_id(repository.generate_id())

def test_exportar_tempo_medio_zero_meses():
    # Adoção no mesmo mês da entrada: o tempo médio é 0, um resultado válido
    animal_recente = Cachorro(
        id=2,
        especie="especie",
        nome="Rec",
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
    adocao_recente = Adocao(
        id=1,
        animal=animal_recente,
        adotante=adotante,
        taxa=10,
        pago=False,
        data=datetime.now(),
    )
    relatorio = TaxaTempoMedioEntradaAdocao(
        id=taxa_tempo_medio_repository.generate_id(),
        data=datetime.now(),
        nome="Tempo medio zero",
        adocoes=[adocao_recente],
    )
    relatorio.gerar()

    assert relatorio.exportar()


# Testes Relatorio TaxaDevolucoes

taxa_devolucoes_id = taxa_devolucoes_repository.generate_id()

taxa_devolucoes = criar_taxa_devolucoes(taxa_devolucoes_id)

def test_generate_id_taxa_devolucoes():
    assert taxa_devolucoes.id == taxa_devolucoes_id

def test_create_taxa_devolucoes():

    assert taxa_devolucoes_repository.create(taxa_devolucoes)


def test_create_duplicado_taxa_devolucoes():
    duplicado = criar_taxa_devolucoes(taxa_devolucoes_id)

    with pytest.raises(Exception, match="já cadastrad"):
        taxa_devolucoes_repository.create(duplicado)

def test_get_all_taxa_devolucoes():
    relatorios = taxa_devolucoes_repository.get_all()
    assert len(relatorios) >= 1

def test_get_by_id_taxa_devolucoes():
    getted_relatorio = taxa_devolucoes_repository.get_by_id(taxa_devolucoes_id)

    assert isinstance(getted_relatorio, TaxaDevolucoes)
    assert getted_relatorio.id == taxa_devolucoes_id
    assert len(getted_relatorio.adocoes) == 1
    assert len(getted_relatorio.devolucoes) == 1
    assert type(getted_relatorio.adocoes[0].animal).__name__ == "Cachorro"
    assert type(getted_relatorio.devolucoes[0].animal).__name__ == "Cachorro"
    assert type(getted_relatorio.devolucoes[0].adotante).__name__ == "Adotante"
    assert getted_relatorio.taxa == "100.00%"

def test_get_by_id_inexistente_taxa_devolucoes():
    with pytest.raises(NaoCadastradoError):
        taxa_devolucoes_repository.get_by_id(taxa_devolucoes_repository.generate_id())

def test_update_taxa_devolucoes():
    getted_relatorio = taxa_devolucoes_repository.get_by_id(taxa_devolucoes_id)

    getted_relatorio.nome = "Nome atualizado"

    taxa_devolucoes_repository.update(getted_relatorio)

    new_relatorio = taxa_devolucoes_repository.get_by_id(taxa_devolucoes_id)

    assert new_relatorio.nome == getted_relatorio.nome

def test_update_inexistente_taxa_devolucoes():
    inexistente = criar_taxa_devolucoes(taxa_devolucoes_repository.generate_id())

    with pytest.raises(NaoCadastradoError):
        taxa_devolucoes_repository.update(inexistente)

def test_delete_by_id_taxa_devolucoes():
    deleted_id = taxa_devolucoes_repository.generate_id()
    deleted_relatorio = criar_taxa_devolucoes(deleted_id)

    taxa_devolucoes_repository.create(deleted_relatorio)

    taxa_devolucoes_repository.delete_by_id(deleted_id)

    with pytest.raises(NaoCadastradoError):
        taxa_devolucoes_repository.get_by_id(deleted_id)

def test_delete_by_id_inexistente_taxa_devolucoes():
    with pytest.raises(NaoCadastradoError):
        taxa_devolucoes_repository.delete_by_id(taxa_devolucoes_repository.generate_id())


# Testes comuns (RelatorioRepository): generate_id e delete_all

TODOS_REPOSITORIES = [
    top5_repository,
    taxa_especies_repository,
    taxa_porte_repository,
    taxa_tempo_medio_repository,
    taxa_devolucoes_repository,
]

@pytest.mark.parametrize("repository", TODOS_REPOSITORIES)
def test_generate_id_incrementa(repository):
    # Após os testes de create, o próximo id deve ser maior que todos os existentes
    ids = [int(i) for i in repository.get_data().keys()]
    assert repository.generate_id() == max(ids) + 1

@pytest.mark.parametrize("repository", TODOS_REPOSITORIES)
def test_delete_all_sem_confirmacao(repository):
    with pytest.raises(Exception, match="Operação não confirmada"):
        repository.delete_all(False)

    # Nada pode ter sido apagado
    assert repository.get_data()
