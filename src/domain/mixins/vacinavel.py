from src.domain.models.auxiliares import Vacina
from src.domain.exceptions import TipagemError


class VacinavelMixin:
    """Classe mixin com informações para animais vacináveis

    A classe é utilizada para agrupar métodos e atributos comuns aos animais
    que tomam vacina no sistema

    Attributes:
        vacinas (list): Vacinas tomadas pelo animal
    """

    def __init__(self, *, vacinas: list[Vacina] = []):
        self.vacinas = vacinas

    def vacinar(self, vacina: Vacina) -> None:
        """Adiciona uma vacina à agenda"""
        if not isinstance(vacina, Vacina):
            # Garante que uma vacina válida foi passada como parâmetro
            raise TipagemError("Vacina", vacina)

        # Adiciona à lista de vacinas
        self.vacinas.append(vacina)

    def get_vacinas(self) -> list[Vacina]:
        """Retorna uma lista de dicionários com as vacinas"""

        return self.vacinas
