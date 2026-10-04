from src.domain.exceptions import ValorForaDoIntervaloError


class AdestravelMixin:
    """Classe mixin com informações para animais adestráveis

    A classe é utilizada para agrupar métodos e atributos comuns aos animais
    que podem ser adestrados no sistema.

    Attributes:
        nivel_adestramento (int): Nível de adestramento do animal.
    """

    def __init__(self, *, nivel_adestramento: int):
        if nivel_adestramento < 0 or nivel_adestramento > 3:
            raise ValorForaDoIntervaloError("nivel_adestramento", nivel_adestramento)

        self.__nivel_adestramento: int = (
            nivel_adestramento  # apenas leitura ou alteração via adestrar (privado)
        )

    @property
    def nivel_adestramento(self):
        return self.__nivel_adestramento

    def adestrar(self):
        if self.nivel_adestramento >= 3:
            return

        self.__nivel_adestramento += 1
