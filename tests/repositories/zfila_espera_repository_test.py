# Declaro utilização de IA para a revisão de código e geração dos testes unitários abaixo
# IA utilizada: claude
"""
Os seguintes testes foram gerados a partir do mesmo chat
utilizado nos testes de RelatorioRepository

O prompt utilizado segue comentado no arquivo 'relatorio_repository_test.py'
"""

# Declaro utilização de IA para adequação às alterações realizadas durante 
# a codificação da API de Relatorio
# IA utilizada: Claude
# Prompt: 
"""
Continuação do chat utilizado para os testes de Relatório Service
"""

# Testes posteriormente adequados à versão atual do model e do repository:
# - FilaEspera exige duracao_reserva e pesos; EntradaFila não possui mais tempo_espera
# - get_all e get_by_animal_id recebem os pesos de compatibilidade
# - entradas expiradas (por data) e de adotantes removidos são descartadas e a limpeza é espelhada no banco

from src.domain import Adotante, Cachorro, FilaEspera, EntradaFila
from src.config import PesosCompatibilidade
from src.repositories import FilaEsperaRepository, PessoaRespository, AnimalRepository
from src.domain.exceptions import NaoCadastradoError, NaoEncontradoError, TipagemError

from random import randint
from datetime import datetime, timedelta
from pathlib import Path
import json
import pytest

# Arquivos exclusivos desta suíte: a fila guarda apenas referências (id do
# animal e email do adotante), então animais e adotantes precisam existir nos
# respectivos bancos. Arquivos próprios evitam interferência de outros testes.
cachorro_path = "tests/data/animal/cachorro_fila_teste.json"
adotante_path = "tests/data/pessoa/adotante_fila_teste.json"
fila_path = "tests/data/fila_espera/fila_espera_teste.json"

# Garante que as pastas dos arquivos fictícios existem
for pasta in ("animal", "pessoa", "fila_espera"):
    Path(f"tests/data/{pasta}").mkdir(parents=True, exist_ok=True)

fila_repository = FilaEsperaRepository(fila_path, Cachorro, cachorro_path, adotante_path) # type: ignore[arg-type]
animal_repository = AnimalRepository(cachorro_path, Cachorro) # type: ignore[arg-type]
adotante_repository = PessoaRespository(adotante_path, Adotante) # type: ignore[arg-type]

# O model e o repository dependem dos pesos de compatibilidade e da duração da reserva
pesos = PesosCompatibilidade(
    nome="pesos compatibilidade",
    data_modificacao=datetime.now(),
    peso_porte_moradia=0.2,
    peso_experiencia_temperamento=0.3,
    peso_tempo_livre_energia=0.2,
    peso_criancas_temperamento=0.3,
)
duracao_reserva = 7


# Funções auxiliares

def criar_cachorro(id):
    return Cachorro(
        id=id,
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

def criar_adotante(email):
    return Adotante(
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

def criar_fila(animal):
    """Cria uma fila vazia com a duração de reserva e os pesos de teste"""
    return FilaEspera(animal=animal, duracao_reserva=duracao_reserva, pesos=pesos, fila=[])

def novo_id_animal():
    return randint(1, 1000000000)

def novo_email():
    return f"email{randint(1, 1000000000)}@gmail.com"

def criar_e_salvar_cachorro():
    """Cria um cachorro novo já persistido (o create da fila exige que o animal exista)"""
    novo_cachorro = criar_cachorro(novo_id_animal())
    animal_repository.create(novo_cachorro)
    return novo_cachorro

def criar_e_salvar_adotante():
    """Cria um adotante novo já persistido e o retorna como o repository o devolve"""
    novo_email_adotante = novo_email()
    adotante_repository.create(criar_adotante(novo_email_adotante))
    return adotante_repository.get_by_email(novo_email_adotante)  # type: ignore[arg-type]

def ler_registro_bruto(animal_id):
    """Lê o registro da fila exatamente como está gravado no json"""
    with open(fila_path, encoding="utf-8") as file:
        return json.load(file)[str(animal_id)]

# Ajuste os nomes dos métodos abaixo caso os repositories usem outro nome
def remover_animal(id):
    animal_repository.delete_by_id(id)

def remover_adotante(email):
    adotante_repository.delete_by_email(email)


# Pré-requisitos: animal e adotantes persistidos nos bancos fictícios

animal_id = novo_id_animal()
cachorro = criar_cachorro(animal_id)
animal_repository.create(cachorro)

email = novo_email()
email2 = novo_email()

adotante_repository.create(criar_adotante(email))
adotante_repository.create(criar_adotante(email2))

adotante = adotante_repository.get_by_email(email)  # type: ignore[arg-type]
adotante2 = adotante_repository.get_by_email(email2)  # type: ignore[arg-type]


def setup_module():
    # Garante um banco de filas limpo: registros gravados em um formato anterior
    # (ex.: com tempo_espera) quebrariam o carregamento das filas
    fila_repository.delete_all(True)


def test_pre_requisitos_persistidos():
    # Se este teste falhar, o problema está na preparação, não no FilaEsperaRepository
    assert animal_repository.get_by_id(animal_id).id == animal_id
    assert adotante_repository.get_by_email(email).email == email  # type: ignore[arg-type]


# Testes FilaEspera

# fila=[] explícito: o comportamento de fila=None é testado separadamente
fila = criar_fila(cachorro)
if adotante:
    fila.add(adotante)

def test_create_fila():
    assert fila_repository.create(fila)

def test_create_persiste_referencias_fila():
    registro = ler_registro_bruto(animal_id)

    # A fila guarda apenas referências: id do animal e email dos adotantes
    assert registro["animal"] == animal_id
    assert registro["duracao_reserva"] == duracao_reserva
    assert len(registro["fila"]) == 1
    assert registro["fila"][0]["adotante"] == email
    assert set(registro["fila"][0].keys()) == {"adotante", "compatibilidade", "data_inicial", "data_expiracao"}

def test_create_duplicado_fila():
    with pytest.raises(Exception, match="já possui uma fila de espera"):
        fila_repository.create(criar_fila(cachorro))

def test_create_animal_nao_persistido_fila():
    nao_persistido = criar_cachorro(novo_id_animal())

    # Não é possível criar fila para um animal que não existe no banco
    with pytest.raises(Exception):
        fila_repository.create(criar_fila(nao_persistido))

    # E nada pode ter sido gravado
    with pytest.raises(NaoCadastradoError):
        fila_repository.get_by_animal_id(nao_persistido.id, pesos)

def test_get_all_fila():
    filas = fila_repository.get_all(pesos)
    assert len(filas) >= 1

def test_get_by_animal_id_fila():
    getted_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    assert isinstance(getted_fila, FilaEspera)
    assert getted_fila.animal.id == animal_id
    assert type(getted_fila.animal).__name__ == "Cachorro"
    assert getted_fila.duracao_reserva == duracao_reserva
    # Os pesos não são persistidos: são os recebidos pelo repository
    assert getted_fila.pesos is pesos
    assert len(getted_fila) == 1

    entrada = getted_fila.proximo()

    assert isinstance(entrada, EntradaFila)
    assert type(entrada.adotante).__name__ == "Adotante"
    assert entrada.adotante.email == email
    assert isinstance(entrada.data_inicial, datetime)
    assert isinstance(entrada.data_expiracao, datetime)
    assert entrada.compatibilidade == fila.proximo().compatibilidade

def test_get_by_animal_id_str_fila():
    # O id do animal pode chegar como str (ex.: parâmetro de rota da API)
    getted_fila = fila_repository.get_by_animal_id(str(animal_id), pesos)
    assert getted_fila.animal.id == animal_id

def test_get_by_animal_id_inexistente_fila():
    with pytest.raises(NaoCadastradoError):
        fila_repository.get_by_animal_id(0, pesos)

def test_update_fila():
    getted_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    getted_fila.add(adotante2)

    fila_repository.update(getted_fila)

    new_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    assert len(new_fila) == 2
    assert new_fila.get_fila() == getted_fila.get_fila()

def test_update_duracao_reserva_fila():
    getted_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    getted_fila.duracao_reserva = 10

    fila_repository.update(getted_fila)

    new_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    assert new_fila.duracao_reserva == 10

def test_update_remove_adotante_fila():
    getted_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    getted_fila.remove(adotante2)

    fila_repository.update(getted_fila)

    new_fila = fila_repository.get_by_animal_id(animal_id, pesos)

    assert len(new_fila) == 1
    assert new_fila.proximo().adotante.email == email

def test_update_inexistente_fila():
    inexistente = criar_fila(criar_cachorro(novo_id_animal()))

    with pytest.raises(NaoCadastradoError):
        fila_repository.update(inexistente)

def test_delete_by_animal_id_fila():
    deleted_cachorro = criar_e_salvar_cachorro()

    fila_repository.create(criar_fila(deleted_cachorro))

    fila_repository.delete_by_animal_id(deleted_cachorro.id)

    with pytest.raises(NaoCadastradoError):
        fila_repository.get_by_animal_id(deleted_cachorro.id, pesos)

def test_delete_by_animal_id_inexistente_fila():
    with pytest.raises(NaoCadastradoError):
        fila_repository.delete_by_animal_id(0)


# Testes de referências quebradas (animal ou adotante removidos dos bancos)

def test_get_by_animal_id_animal_removido_fila():
    orfao = criar_e_salvar_cachorro()

    fila_repository.create(criar_fila(orfao))

    remover_animal(orfao.id)

    # A fila de um animal removido deixa de existir
    with pytest.raises(NaoCadastradoError):
        fila_repository.get_by_animal_id(orfao.id, pesos)

    # E foi limpa do banco
    with pytest.raises(NaoCadastradoError):
        fila_repository.delete_by_animal_id(orfao.id)

def test_get_all_ignora_fila_de_animal_removido():
    orfao = criar_e_salvar_cachorro()

    fila_repository.create(criar_fila(orfao))

    remover_animal(orfao.id)

    filas = fila_repository.get_all(pesos)

    # Nenhuma fila retornada pode estar com o animal quebrado
    assert len(filas) >= 1
    assert all(isinstance(f.animal, Cachorro) for f in filas)
    assert orfao.id not in [f.animal.id for f in filas]

def test_get_by_animal_id_adotante_removido_fila():
    animal = criar_e_salvar_cachorro()
    adotante_removido = criar_e_salvar_adotante()

    fila_teste = criar_fila(animal)
    fila_teste.add(adotante)
    fila_teste.add(adotante_removido)

    fila_repository.create(fila_teste)

    remover_adotante(adotante_removido.email)

    getted_fila = fila_repository.get_by_animal_id(animal.id, pesos)

    # Apenas entradas com adotante existente são consideradas
    assert len(getted_fila) == 1
    assert getted_fila.proximo().adotante.email == email

    # A limpeza é espelhada no banco
    assert len(ler_registro_bruto(animal.id)["fila"]) == 1

    fila_repository.delete_by_animal_id(animal.id)


# Testes de expiração das entradas

def test_get_by_animal_id_entrada_expirada_fila():
    animal = criar_e_salvar_cachorro()
    adotante_expirado = criar_e_salvar_adotante()

    fila_teste = criar_fila(animal)
    fila_teste.add(adotante)
    # Entrada adicionada diretamente, já expirada desde ontem
    fila_teste.fila.append(EntradaFila(
        adotante=adotante_expirado,
        compatibilidade=1.0,
        data_inicial=datetime.now() - timedelta(days=10),
        data_expiracao=datetime.now() - timedelta(days=1),
    ))

    fila_repository.create(fila_teste)
    assert len(ler_registro_bruto(animal.id)["fila"]) == 2

    getted_fila = fila_repository.get_by_animal_id(animal.id, pesos)

    # Entradas expiradas são descartadas
    assert len(getted_fila) == 1
    assert getted_fila.proximo().adotante.email == email

    # A limpeza é espelhada no banco
    assert len(ler_registro_bruto(animal.id)["fila"]) == 1

    fila_repository.delete_by_animal_id(animal.id)

def test_get_by_animal_id_entrada_expira_hoje_mantida_fila():
    animal = criar_e_salvar_cachorro()
    adotante_hoje = criar_e_salvar_adotante()

    fila_teste = criar_fila(animal)
    # A expiração é comparada por dia: uma entrada que expira hoje ainda é válida
    fila_teste.fila.append(EntradaFila(
        adotante=adotante_hoje,
        compatibilidade=1.0,
        data_inicial=datetime.now() - timedelta(days=7),
        data_expiracao=datetime.now(),
    ))

    fila_repository.create(fila_teste)

    getted_fila = fila_repository.get_by_animal_id(animal.id, pesos)

    assert len(getted_fila) == 1
    assert getted_fila.proximo().adotante.email == adotante_hoje.email

    fila_repository.delete_by_animal_id(animal.id)

def test_get_by_animal_id_entrada_nao_expirada_mantida_fila():
    animal = criar_e_salvar_cachorro()

    fila_teste = criar_fila(animal)
    fila_teste.add(adotante)

    fila_repository.create(fila_teste)

    getted_fila = fila_repository.get_by_animal_id(animal.id, pesos)

    assert len(getted_fila) == 1
    assert getted_fila.proximo().data_expiracao > datetime.now()

    fila_repository.delete_by_animal_id(animal.id)


# Testes de comportamento do domínio que afetam a persistência

def test_fila_nao_compartilha_lista_none():
    # Duas filas criadas com fila=None não podem compartilhar a mesma lista
    fila_a = FilaEspera(animal=criar_cachorro(1), duracao_reserva=duracao_reserva, pesos=pesos, fila=None)
    fila_b = FilaEspera(animal=criar_cachorro(2), duracao_reserva=duracao_reserva, pesos=pesos, fila=None)

    fila_a.add(adotante)

    assert len(fila_a) == 1
    assert len(fila_b) == 0

def test_add_tipo_invalido_fila():
    fila_teste = criar_fila(criar_cachorro(1))

    with pytest.raises(TipagemError):
        fila_teste.add("nao_e_um_adotante")  # type: ignore[arg-type]

    assert len(fila_teste) == 0

def test_add_duplicado_fila():
    fila_teste = criar_fila(criar_cachorro(1))

    fila_teste.add(adotante)

    with pytest.raises(Exception, match="duas vezes"):
        fila_teste.add(adotante)

    assert len(fila_teste) == 1

def test_add_duplicado_instancia_recarregada_fila():
    fila_teste = criar_fila(criar_cachorro(1))

    fila_teste.add(adotante)

    # Mesmo adotante (mesmo email), mas outra instância, como acontece
    # ao carregar a fila do repository
    mesmo_adotante = adotante_repository.get_by_email(email)  # type: ignore[arg-type]

    with pytest.raises(Exception, match="duas vezes"):
        fila_teste.add(mesmo_adotante)

    assert len(fila_teste) == 1

def test_remove_tipo_invalido_fila():
    fila_teste = criar_fila(criar_cachorro(1))

    with pytest.raises(TipagemError):
        fila_teste.remove("nao_e_um_adotante")  # type: ignore[arg-type]

def test_remove_inexistente_fila():
    fila_teste = criar_fila(criar_cachorro(1))

    with pytest.raises(NaoEncontradoError):
        fila_teste.remove(adotante)

def test_contains_tipo_invalido_fila():
    # Um objeto que não é EntradaFila não pode ser considerado "contido" na fila
    assert adotante not in fila


# Testes comuns: delete_all

def test_delete_all_sem_confirmacao():
    with pytest.raises(Exception, match="Operação não confirmada"):
        fila_repository.delete_all(False)

    # Nada pode ter sido apagado
    assert len(fila_repository.get_all(pesos)) >= 1
