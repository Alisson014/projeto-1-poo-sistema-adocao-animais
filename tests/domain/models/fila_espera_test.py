# Declaro utilização de IA para adequação às alterações realizadas durante 
# a codificação da API de Relatorio
# IA utilizada: Claude
# Prompt: 
"""
Continuação do chat utilizado para os testes de Relatório Service
"""

# Testes posteriormente adequados à versão atual do model:
# - EntradaFila não possui mais tempo_espera; recebe data_expiracao (obrigatória) e data_inicial
# - FilaEspera exige duracao_reserva e pesos
# - a compatibilidade é calculada por get_compatibilidade e a fila é ordenada de forma decrescente

from src.domain.models import EntradaFila, FilaEspera, Adotante, Cachorro
from src.domain.exceptions import *
from src.config import PesosCompatibilidade
from src.utils import get_compatibilidade

from datetime import datetime, timedelta

import pytest

cachorro = Cachorro(
    id=0,
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

pesos = PesosCompatibilidade(
    nome="pesos compatibilidade",
    data_modificacao=datetime.now(),
    peso_porte_moradia=0.2,
    peso_experiencia_temperamento=0.3,
    peso_tempo_livre_energia=0.2,
    peso_criancas_temperamento=0.3,
)

DURACAO_RESERVA = 7


def novo_adotante(
    email: str = "email@gmail.com",
    experiencia: str = "AVANCADO",
    tempo_livre_min: int = 50,
    possui_criancas: bool = True,
    outros_animais: bool = True,
) -> Adotante:
    return Adotante(
        nome="teste",
        email=email,
        idade=18,
        moradia="CASA_COM_QUINTAL",
        experiencia=experiencia,
        tempo_livre_min=tempo_livre_min,
        possui_criancas=possui_criancas,
        outros_animais=outros_animais,
        area_util=50,
    )

adotante = novo_adotante()

def nova_fila(duracao_reserva: int = DURACAO_RESERVA) -> FilaEspera:
    # fila=[] explícito: o comportamento de fila=None é testado separadamente
    return FilaEspera(animal=cachorro, duracao_reserva=duracao_reserva, pesos=pesos, fila=[])

def nova_entrada(compatibilidade: float = 80.0, email: str = "email@gmail.com") -> EntradaFila:
    # Datas fixas para que a comparação via __eq__ (baseada em repr) seja determinística
    return EntradaFila(
        adotante=novo_adotante(email),
        compatibilidade=compatibilidade,
        data_inicial=datetime(2025, 4, 1, 10, 0, 0),
        data_expiracao=datetime(2025, 4, 8, 10, 0, 0),
    )


# Testes de EntradaFila
def test_cria_entrada_fila():
    entrada = EntradaFila(
        adotante=adotante,
        compatibilidade=100,
        data_expiracao=datetime.now() + timedelta(days=DURACAO_RESERVA),
    )

    assert entrada
    assert entrada.adotante == adotante
    assert entrada.compatibilidade == 100
    assert isinstance(entrada.data_inicial, datetime)
    assert isinstance(entrada.data_expiracao, datetime)
    assert entrada.__str__()

def test_entrada_fila_datas_como_string():
    # O repository carrega as datas do json como str
    entrada = EntradaFila(
        adotante=adotante,
        compatibilidade=100,
        data_inicial="2025-04-01 10:00:00",
        data_expiracao="2025-04-08 10:00:00",
    )

    assert entrada.data_inicial == datetime(2025, 4, 1, 10, 0, 0)
    assert entrada.data_expiracao == datetime(2025, 4, 8, 10, 0, 0)

def test_entrada_fila_to_dict():
    entrada = nova_entrada(compatibilidade=80.0)

    assert entrada.to_dict() == {
        "adotante": "email@gmail.com",
        "compatibilidade": 80.0,
        "data_inicial": "2025-04-01 10:00:00",
        "data_expiracao": "2025-04-08 10:00:00",
    }

def test_entrada_fila_from_dict():
    # Formato recebido do repository: adotante já carregado e datas como str
    entrada = EntradaFila.from_dict({
        "adotante": adotante,
        "compatibilidade": 80.0,
        "data_inicial": "2025-04-01 10:00:00",
        "data_expiracao": "2025-04-08 10:00:00",
    })

    assert entrada == nova_entrada(compatibilidade=80.0)

def test_entrada_fila_adotante_somente_leitura():
    entrada = nova_entrada()

    with pytest.raises(AttributeError):
        entrada.adotante = novo_adotante("outro@gmail.com")  # type: ignore[misc]

def test_entrada_fila_compatibilidade_somente_leitura():
    entrada = nova_entrada()

    with pytest.raises(AttributeError):
        entrada.compatibilidade = 1  # type: ignore[misc]

def test_entrada_fila_eq():
    assert nova_entrada(80.0) == nova_entrada(80.0)
    assert nova_entrada(80.0) != nova_entrada(70.0)

def test_entrada_fila_eq_tipo_invalido():
    assert (nova_entrada() == "nao_e_uma_entrada") is False

def test_entrada_fila_lt():
    assert nova_entrada(70.0) < nova_entrada(80.0)
    assert not nova_entrada(80.0) < nova_entrada(70.0)

def test_entrada_fila_lt_tipo_invalido():
    with pytest.raises(TypeError):
        nova_entrada() < 1  # type: ignore[operator]


# Testes de FilaEspera
def test_cria_fila_espera():
    fila_espera = nova_fila()

    assert fila_espera.__str__()
    assert fila_espera.animal == cachorro
    assert fila_espera.duracao_reserva == DURACAO_RESERVA
    assert fila_espera.pesos is pesos
    assert len(fila_espera) == 0

def test_fila_espera_nao_compartilha_lista_none():
    # Duas filas criadas com fila=None não podem compartilhar a mesma lista
    fila_a = FilaEspera(animal=cachorro, duracao_reserva=DURACAO_RESERVA, pesos=pesos, fila=None)
    fila_b = FilaEspera(animal=cachorro, duracao_reserva=DURACAO_RESERVA, pesos=pesos, fila=None)

    fila_a.add(adotante)

    assert len(fila_a) == 1
    assert len(fila_b) == 0

def test_fila_espera_animal_somente_leitura():
    fila_espera = nova_fila()

    with pytest.raises(AttributeError):
        fila_espera.animal = cachorro  # type: ignore[misc]

def test_fila_espera_adiciona_entrada():
    fila_espera = nova_fila()
    fila_espera.add(adotante=adotante)

    assert len(fila_espera.get_fila()) == 1

    entrada = fila_espera.proximo()

    assert isinstance(entrada, EntradaFila)
    assert entrada.adotante == adotante
    # A compatibilidade é calculada a partir do animal, do adotante e dos pesos
    assert entrada.compatibilidade == get_compatibilidade(cachorro, adotante, pesos)

def test_fila_espera_adiciona_entrada_datas_pela_duracao_reserva():
    fila_espera = nova_fila(duracao_reserva=10)
    fila_espera.add(adotante=adotante)

    entrada = fila_espera.proximo()

    # data_expiracao = data_inicial + duracao_reserva dias
    assert (entrada.data_expiracao - entrada.data_inicial).days == 10

def test_fila_espera_adiciona_entrada_ordem_decrescente_compatibilidade():
    fila_espera = nova_fila()

    fila_espera.add(novo_adotante("a@gmail.com", experiencia="INICIANTE", tempo_livre_min=50, possui_criancas=True))
    fila_espera.add(novo_adotante("b@gmail.com", experiencia="AVANCADO", tempo_livre_min=120, possui_criancas=False))
    fila_espera.add(novo_adotante("c@gmail.com", experiencia="INICIANTE", tempo_livre_min=120, possui_criancas=False))
    fila_espera.add(novo_adotante("d@gmail.com", experiencia="AVANCADO", tempo_livre_min=50, possui_criancas=True))

    compatibilidades = [e.compatibilidade for e in fila_espera.fila]

    assert len(fila_espera) == 4
    assert compatibilidades == sorted(compatibilidades, reverse=True)

def test_fila_espera_adiciona_entrada_empate_mantem_ordem_de_chegada():
    fila_espera = nova_fila()

    # Mesmo perfil -> mesma compatibilidade
    primeiro = novo_adotante("primeiro@gmail.com")
    segundo = novo_adotante("segundo@gmail.com")

    fila_espera.add(primeiro)
    fila_espera.add(segundo)

    assert fila_espera.fila[0].compatibilidade == fila_espera.fila[1].compatibilidade
    assert fila_espera.proximo().adotante == primeiro
    assert fila_espera.fila[1].adotante == segundo

def test_fila_espera_adiciona_entrada_tipo_invalido():
    fila_espera = nova_fila()

    with pytest.raises(TipagemError):
        fila_espera.add("nao_e_um_adotante")  # type: ignore[arg-type]

    assert len(fila_espera) == 0

def test_fila_espera_adiciona_entrada_duplicada():
    fila_espera = nova_fila()
    fila_espera.add(adotante)

    with pytest.raises(Exception, match="duas vezes"):
        fila_espera.add(adotante)

    assert len(fila_espera) == 1

def test_fila_espera_remove_entrada():
    fila_espera = nova_fila()
    fila_espera.add(adotante=adotante)
    fila_espera.remove(adotante=adotante)

    assert len(fila_espera.get_fila()) == 0

def test_fila_espera_remove_entrada_error():
    with pytest.raises(NaoEncontradoError):
        fila_espera = nova_fila()
        fila_espera.add(adotante=adotante)
        adotante2 = novo_adotante("email2@gmail.com")
        fila_espera.remove(adotante=adotante2)

def test_fila_espera_remove_entrada_tipo_invalido():
    fila_espera = nova_fila()

    with pytest.raises(TipagemError):
        fila_espera.remove("nao_e_um_adotante")  # type: ignore[arg-type]

def test_fila_espera_proximo_fila_vazia():
    assert nova_fila().proximo() is None

def test_fila_espera_proximo_maior_compatibilidade():
    fila_espera = nova_fila()

    fila_espera.add(novo_adotante("a@gmail.com", experiencia="INICIANTE", tempo_livre_min=50, possui_criancas=True))
    fila_espera.add(novo_adotante("b@gmail.com", experiencia="AVANCADO", tempo_livre_min=120, possui_criancas=False))
    fila_espera.add(novo_adotante("c@gmail.com", experiencia="INICIANTE", tempo_livre_min=120, possui_criancas=False))

    proximo = fila_espera.proximo()

    assert proximo == fila_espera.fila[0]
    assert proximo.compatibilidade == max(e.compatibilidade for e in fila_espera.fila)

def test_fila_espera_get_fila():
    fila_espera = nova_fila()
    fila_espera.add(adotante)

    res = fila_espera.get_fila()

    assert len(res) == 1
    assert isinstance(res[0], dict)
    assert res[0]["adotante"] == adotante.email
    assert set(res[0].keys()) == {"adotante", "compatibilidade", "data_inicial", "data_expiracao"}

def test_fila_espera_to_dict():
    fila_espera = nova_fila()
    fila_espera.add(adotante)

    res = fila_espera.to_dict()

    # A fila guarda apenas referências: id do animal e email dos adotantes
    assert res["animal"] == cachorro.id
    assert res["duracao_reserva"] == DURACAO_RESERVA
    assert res["fila"] == fila_espera.get_fila()
    assert "pesos" not in res

def test_fila_espera_from_dict():
    fila_espera = FilaEspera.from_dict({
        "animal": cachorro,
        "duracao_reserva": 5,
        "pesos": pesos,
        "fila": [],
    })

    assert fila_espera.animal == cachorro
    assert fila_espera.duracao_reserva == 5
    assert fila_espera.pesos is pesos
    assert len(fila_espera) == 0

def test_fila_espera_len():
    fila_espera = nova_fila()
    assert len(fila_espera) == 0

    fila_espera.add(adotante)
    assert len(fila_espera) == 1

def test_fila_espera_contains():
    fila_espera = nova_fila()
    fila_espera.add(adotante)

    assert fila_espera.fila[0] in fila_espera
    assert nova_entrada(compatibilidade=1.0) not in fila_espera

def test_fila_espera_contains_tipo_invalido():
    # Um objeto que não é EntradaFila não pode ser considerado "contido" na fila
    fila_espera = nova_fila()
    fila_espera.add(adotante)

    assert adotante not in fila_espera

def test_fila_espera_lt():
    fila_a = nova_fila()
    fila_b = nova_fila()
    fila_b.add(adotante)

    assert fila_a < fila_b
    assert not fila_b < fila_a

def test_fila_espera_lt_tipo_invalido():
    with pytest.raises(TypeError):
        nova_fila() < 1  # type: ignore[operator]
