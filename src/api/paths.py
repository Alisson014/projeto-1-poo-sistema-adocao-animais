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

