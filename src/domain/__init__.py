from src.domain.models import Animal, Cachorro, Calopsita, Coelho, Gato
from src.domain.models import Pessoa, Adotante
from src.domain.models import Registro, Reserva, Devolucao, Adocao
from src.domain.models import Vacina, Evento
from src.domain.models import Quarentena
from src.domain.models import EntradaFila, FilaEspera
from src.domain.models import Top5MaisAdotaveis, TaxaAdocaoEspecies, TaxaAdocaoPorte, TaxaDevolucoes, TaxaTempoMedioEntradaAdocao

from src.domain.mixins import AdestravelMixin, VacinavelMixin

__all__ = [
    "Animal", 
    "Cachorro", 
    "Calopsita", 
    "Coelho", 
    "Gato",
    "Pessoa", 
    "Adotante",
    "Registro", 
    "Reserva", 
    "Devolucao", 
    "Adocao",
    "Vacina", 
    "Evento",
    "Quarentena",
    "EntradaFila", 
    "FilaEspera",
    "Top5MaisAdotaveis", 
    "TaxaAdocaoEspecies", 
    "TaxaAdocaoPorte", 
    "TaxaDevolucoes", 
    "TaxaTempoMedioEntradaAdocao",
    "AdestravelMixin", 
    "VacinavelMixin"
]
