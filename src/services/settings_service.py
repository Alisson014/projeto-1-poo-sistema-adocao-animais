from typing import Literal

from ..config import IdadeMinima, DuracaoReserva, PesosCompatibilidade, PorteXArea, Politica
from ..repositories import PoliticaRepository


class PoliticaService:
    """Classe para modelar os serviços referentes ao domínio de Politica

    A classe é responsável por garantir o cumprimento das regras de negócio
    e a utilização do repository

    Attributes:
        repository (PoliticaRepository): Repository do relatório Top5MaisAdotaveis
        class_initializer (dict[str, type[Politica]]): Mapeia as classes aos seus models
    """
    def __init__(self, path):
        self.repository = PoliticaRepository(path)
        self.class_initializer: dict[str, type[Politica]] = {
            "IdadeMinima": IdadeMinima,
            "DuracaoReserva": DuracaoReserva,
            "PesosCompatibilidade": PesosCompatibilidade,
            "PorteXArea": PorteXArea,
        }

    def create(self, politica_name: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"], politica_data:dict):
        model = self.class_initializer[politica_name]

        # As validações são feitas no escopo da classe model
        politica = model.from_dict(politica_data)

        self.repository.create(politica)

        return politica

    def get_all(self):
        return self.repository.get_all()

    def get_by_name(self, politica_name: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"]):
        return self.repository.get_by_name(politica_name)

    def update(self, politica_name: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"], politica_data:dict):
        updated_politica = self.repository.get_by_name(politica_name)

        for key, value in politica_data.items():
            if hasattr(updated_politica, key) and key:
                setattr(updated_politica, key, value)

        self.repository.update(updated_politica)

        return updated_politica

    def delete_by_name(self, politica_name: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"]):
        self.repository.delete_by_name(politica_name)

    def delete_all(self):
        self.repository.delete_all(True)
