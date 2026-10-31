from dataclasses import dataclass
from pathlib import Path

# @dataclass(frozen=True)
# Utilizado para impedir que os atributos destas classes sejam alterados
# Impedindo alteração dos caminhos em execução

# =========================
#  Animal
# =========================

@dataclass(frozen=True)
class AnimalPath:
    # Garante que a pasta exista
    Path("data/animal").mkdir(parents=True, exist_ok=True)

    cachorro = "data/animal/cachorro.json"
    calopsita = "data/animal/calopsita.json"
    coelho = "data/animal/coelho.json"
    gato = "data/animal/gato.json"


# =========================
#  Pessoa
# =========================

@dataclass(frozen=True)
class PessoaPath:
    # Garante que a pasta exista
    Path("data/pessoa").mkdir(parents=True, exist_ok=True)

    adotante = "data/pessoa/adotante.json"


# =========================
#  Politica
# =========================

@dataclass(frozen=True)
class PoliticaPath:

    path = "data/settings.json"


# =========================
#  Quarentena
# =========================

@dataclass(frozen=True)
class QuarentenaPath:
    Path("data/quarentena").mkdir(parents=True, exist_ok=True)

    cachorro = "data/quarentena/q_cachorro.json"
    calopsita = "data/quarentena/q_calopsita.json"
    coelho = "data/quarentena/q_coelho.json"
    gato = "data/quarentena/q_gato.json"

