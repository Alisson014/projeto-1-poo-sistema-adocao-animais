# Padrão de importação: Abstrata, Subclasses...
# Nunca utilizar import * (Para previnir erros de importação circular)

from src.domain.models.animal import Animal, Cachorro, Calopsita, Coelho, Gato
from src.domain.models.auxiliares import Evento, Vacina
from src.domain.models.fila_espera import FilaEspera, EntradaFila
from src.domain.models.pessoa import Pessoa, Adotante
from src.domain.models.quarentena import Quarentena
from src.domain.models.registro import Registro, Adocao, Devolucao, Reserva
from src.domain.models.relatorio import (
    Relatorio,
    TaxaAdocaoEspecies,
    TaxaAdocaoPorte,
    TaxaDevolucoes,
    TaxaTempoMedioEntradaAdocao,
    Top5MaisAdotaveis,
)

__all__ = [
    "Animal",
    "Cachorro",
    "Calopsita",
    "Coelho",
    "Gato",
    "Evento",
    "Vacina",
    "FilaEspera",
    "EntradaFila",
    "Pessoa",
    "Adotante",
    "Registro",
    "Adocao",
    "Devolucao",
    "Reserva",
    "Relatorio",
    "TaxaAdocaoEspecies",
    "TaxaAdocaoPorte",
    "TaxaDevolucoes",
    "TaxaTempoMedioEntradaAdocao",
    "Top5MaisAdotaveis",
]
