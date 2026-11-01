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


# =========================
#  Registro
# =========================

@dataclass(frozen=True)
class RegistroPath:
    Path("data/registro").mkdir(parents=True, exist_ok=True)
    Path("data/registro/adocao").mkdir(parents=True, exist_ok=True)
    Path("data/registro/devolucao").mkdir(parents=True, exist_ok=True)
    Path("data/registro/reserva").mkdir(parents=True, exist_ok=True)

    # Arquivos de adocao
    a_cachorro = "data/registro/adocao/a_cachorro.json"
    a_calopsita = "data/registro/adocao/a_calopsita.json"
    a_coelho = "data/registro/adocao/a_coelho.json"
    a_gato = "data/registro/adocao/a_gato.json"

    # Arquivos de devolucao
    d_cachorro = "data/registro/devolucao/d_cachorro.json"
    d_calopsita = "data/registro/devolucao/d_calopsita.json"
    d_coelho = "data/registro/devolucao/d_coelho.json"
    d_gato = "data/registro/devolucao/d_gato.json"
    
    # Arquivos de reserva
    r_cachorro = "data/registro/reserva/r_cachorro.json"
    r_calopsita = "data/registro/reserva/r_calopsita.json"
    r_coelho = "data/registro/reserva/r_coelho.json"
    r_gato = "data/registro/reserva/r_gato.json"

