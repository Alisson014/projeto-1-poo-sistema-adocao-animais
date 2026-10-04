from src.domain.enums import Moradia, Experiencia
from src.domain.exceptions import (
    EmailInvalidoError,
    TipagemError,
    ValorForaDoIntervaloError,
)


class Pessoa:
    """Clase abstrata para modelar pessoas no sistema

    A classe define os atributos e métodos comuns a todas as pessoas
    cadastradas no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        nome (string): Nome da pessoa.
        email (string): Email para identificar uma pessoa.
        idade (int): Idade da pessoa em anos.
    """

    def __init__(self, *, nome: str, email: str, idade: int):
        self.nome: str = nome
        self.email: str = email  # property setter (privado)
        self.idade: int = idade  # property setter (privado)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        if (
            (not "@" in email)
            or (not "." in email[email.index("@") + 1 :])
            or (len(email) <= 3)
            or (email[0] == "@")
        ):
            raise EmailInvalidoError(email)
        self.__email = email

    @property
    def idade(self) -> int:
        return self.__idade

    @idade.setter
    def idade(self, idade: int):
        if idade < 0:
            raise ValorForaDoIntervaloError("idade", idade)
        self.__idade: int = idade


class Adotante(Pessoa):
    """Classe para modelar adotantes no sistema

    A classe herda atributos de Pessoa e possui
    os próprios atributos específicos.

    Attributes:
        moradia (APARTAMENTO_COM_VARANDA, APARTAMENTO_SEM_VARANDA, CASA_COM_QUINTAL, CASA_SEM_QUINTAL): Tipo de moradia.
        experiencia (INICIANTE, INTERMEDIÁRIO, AVANÇADO): Experiência com animais.
        tempo_livre_min (int): Tempo livre médio em minutos.
        possui_criancas (bool): Indica se pessui crianças ou não.
        outros_animais (bool): Indica se possui outros animais ou não.
        area_util (float): Area útil da residência em metros quadrados.
    """

    def __init__(
        self,
        *,
        nome: str,
        email: str,
        idade: int,
        moradia: str,
        experiencia: str,
        tempo_livre_min: int,
        possui_criancas: bool,
        outros_animais: bool,
        area_util: float,
    ):
        super().__init__(nome=nome, email=email, idade=idade)
        self.moradia: Moradia = moradia  # property setter (privado)
        self.experiencia: Experiencia = experiencia  # property setter (privado)
        self.tempo_livre_min: int = tempo_livre_min  # property setter (privado)
        self.possui_criancas: bool = possui_criancas
        self.outros_animais: bool = outros_animais
        self.area_util: float = area_util  # property setter (privado)

    # __moradia: possui getter e setter para garantir alinhamento à tipagem
    @property
    def moradia(self) -> str:
        return self.__moradia.value

    @moradia.setter
    def moradia(self, moradia: str) -> None:
        try:
            if isinstance(Moradia(moradia), Moradia):
                self.__moradia = Moradia(moradia)
        except ValueError:
            raise TipagemError("Moradia", moradia)

    # __experiencia: possui getter e setter para garantir alinhamento à tipagem
    @property
    def experiencia(self) -> str:
        return self.__experiencia.value

    @experiencia.setter
    def experiencia(self, experiencia: str) -> None:
        try:
            if isinstance(Experiencia(experiencia), Experiencia):
                self.__experiencia = Experiencia(experiencia)
        except ValueError:
            raise TipagemError("Experiencia", experiencia)

    # __tempo_livre_min: possui getter e setter para garantir alinhamento à tipagem
    @property
    def tempo_livre_min(self) -> str:
        return self.__tempo_livre_min

    @tempo_livre_min.setter
    def tempo_livre_min(self, tempo_livre_min):
        if tempo_livre_min < 0:
            raise ValorForaDoIntervaloError("tempo_livre_min", tempo_livre_min)

        self.__tempo_livre_min = tempo_livre_min

    # __area_util: possui getter e setter para garantir alinhamento à tipagem
    @property
    def area_util(self) -> float:
        return self.__area_util

    @area_util.setter
    def area_util(self, area_util):
        if area_util < 0:
            raise ValorForaDoIntervaloError("area_util", area_util)

        self.__area_util = area_util
