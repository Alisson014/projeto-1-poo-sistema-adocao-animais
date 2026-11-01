from .animal_schema import AnimalCreateSchema, CachorroCreateSchema, CachorroResponseSchema, CalopsitaCreateSchema, CalopsitaResponseSchema, CoelhoCreateSchema, CoelhoResponseSchema, GatoCreateSchema, GatoResponseSchema, AnimalResponseUnion
from .auxiliares_schema import EventoSchame, VacinaSchema
from .pessoa_schema import AdotanteSchema
from .politica_schema import PorteXAreaSchema, IdadeMinimaSchema, DuracaoReservaSchema, PesosCompatibilidadeSchema, PoliticaUnion, PoliticaSchema
from .quarentena_schema import QuarentenaCreateSchema, QuarentenaResponseSchema
from .registro_schema import AdocaoCreateSchema, AdocaoResponseSchema, DevolucaoCreateSchema, DevolucaoResponseSchema, ReservaCreateSchema, ReservaResponseSchema, RegistroResponseUnion
from .relatorio_schema import Top5MaisAdotaveisCreateSchema, Top5MaisAdotaveisResponseSchema, TaxaAdocaoCreateSchema, TaxaAdocaoResponseSchema, TaxaTempoMedioEntradaAdocaoResponseSchema, TaxaDevolucoesCreateSchema, TaxaDevolucoesResponseSchema, RelatorioCreateUnion, RelatorioResponseUnion

__all__ = [
    "AnimalCreateSchema",
    "CachorroCreateSchema",
    "CachorroResponseSchema",
    "CalopsitaCreateSchema",
    "CalopsitaResponseSchema",
    "CoelhoCreateSchema",
    "CoelhoResponseSchema",
    "GatoCreateSchema",
    "GatoResponseSchema",
    "AnimalResponseUnion",
    "EventoSchame",
    "VacinaSchema",
    "AdotanteSchema",
    "PorteXAreaSchema",
    "IdadeMinimaSchema",
    "DuracaoReservaSchema",
    "PesosCompatibilidadeSchema",
    "PoliticaSchema",
    "PoliticaUnion",
    "QuarentenaCreateSchema",
    "QuarentenaResponseSchema",
    "AdocaoCreateSchema",
    "AdocaoResponseSchema",
    "DevolucaoCreateSchema",
    "DevolucaoResponseSchema",
    "ReservaCreateSchema",
    "ReservaResponseSchema",
    "RegistroResponseUnion",
    "Top5MaisAdotaveisCreateSchema",
    "Top5MaisAdotaveisResponseSchema",
    "TaxaAdocaoCreateSchema",
    "TaxaAdocaoResponseSchema",
    "TaxaTempoMedioEntradaAdocaoResponseSchema",
    "TaxaDevolucoesCreateSchema",
    "TaxaDevolucoesResponseSchema",
    "RelatorioCreateUnion",
    "RelatorioResponseUnion"
]
