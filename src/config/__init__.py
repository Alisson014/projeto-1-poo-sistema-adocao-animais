# Padrão de importação: Abstrata, Subclasses...
# Nunca utilizar import * (Para previnir erros de importação circular)

from src.config.settings import (
    Politica,
    DuracaoReserva,
    IdadeMinima,
    PesosCompatibilidade,
    PorteXArea,
)
