from src.domain.enums import StatusReserva, MotivoDevolucao
from src.domain.models.animal import Animal
from src.domain.models.pessoa import Adotante
from src.domain.exceptions import TipagemError

from datetime import datetime


class Registro:
    """Classe abstrata para modelar registros no sistema

    A classe define os atributos e métodos comuns a todos os registros
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        id (int): Id único de identificação do registro.
        animal Animal: Animal envolvido.
        adotante Adotante: Adotante envolvido.
    """

    def __init__(self, *, id: int, animal: Animal, adotante: Adotante):
        self.__id: int = id  # Apenas acessado, nunca alterado
        self.__animal: Animal = animal  # Apenas acessado, nunca alterado
        self.__adotante: Adotante = adotante  # Apenas acessado, nunca alterado

    @property
    def id(self) -> int:
        return self.__id

    @property
    def animal(self) -> Animal:
        return self.__animal

    @property
    def adotante(self) -> Adotante:
        return self.__adotante


class Reserva(Registro):
    """Classe para modelar reservas no sistema

    A classe herda atributos de Registro e também possui os próprios
    atributos.

    Attributes:
        data_inicial (date): Data inicial da reserva.
        data_expiracao (date): Data de expiração da reserva.
        status (ATIVA, CANCELADA, EXPIRADA): Status da reserva.
        compatibilidade (float): Compatibilidade entre os Animal e contratante envolvidos.
    """

    def __init__(
        self,
        *,
        id: int,
        animal: Animal,
        adotante: Adotante,
        data_inicial: datetime,
        data_expiracao: datetime,
        status: str,
        compatibilidade: float,
    ):
        super().__init__(id=id, animal=animal, adotante=adotante)
        self.data_inicial: datetime = data_inicial
        self.data_expiracao: datetime = data_expiracao
        self.status: StatusReserva = status  # property setter (privado)
        self.compatibilidade: float = compatibilidade

    @property
    def status(self) -> str:
        return self.__status.value

    @status.setter
    def status(self, status: str) -> None:
        try:
            if isinstance(StatusReserva(status), StatusReserva):
                self.__status = StatusReserva(status)
        except ValueError:
            raise TipagemError("StatusReserva", status)

    def __str__(self) -> str:
        return f"Reserva de {type(self.animal).__name__} {self.animal.nome} por {self.adotante.nome} em {self.data_inicial.day}/{self.data_inicial.month}/{self.data_inicial.year}"

    def __repr__(self) -> str:
        return f"Adocao(id={self.id}, animal={repr(self.animal)}, adotante={repr(self.adotante)}, data_inicial={self.data_inicial}, data_expiracao={self.data_expiracao}, status={self.status}, compatibilidade={self.compatibilidade})"


class Adocao(Registro):
    """Classe para modelar adoções no sistema

    A classe herda atributos de Registro e também possui os próprios
    atributos.

    Attributes:
        taxa (float): Taxa de adoção a ser cobrada.
        pago (bool): Indica se a taxa foi paga ou não.
        data (date): Data da adoção.
    """

    def __init__(
        self,
        *,
        id: int,
        animal: Animal,
        adotante: Adotante,
        taxa: float,
        pago: bool,
        data: datetime,
    ):
        super().__init__(id=id, animal=animal, adotante=adotante)
        self.__taxa: float = taxa  # Pode apenas ser lido
        self.pago: bool = pago
        self.data: datetime = data

    @property
    def taxa(self) -> float:
        return self.__taxa

    def calcular_taxa(self):
        """Método para calcular a taxa de uma adoção"""
        #### Precisa de métricas de políticas para ser implementado

    def gerar_contrato(self) -> str:
        """Retorna o contrato da adoção"""
        return f"Adoção realizada em {self.data.day}/{self.data.month}/{self.data.year}\nValor da taxa:R$ {self.__taxa:.2f}\nPago: {'Sim' if self.pago else 'Não'}"

    def registrar_pagamento(self) -> None:
        self.pago = True

    def __str__(self) -> str:
        return f"Adocao de {type(self.animal).__name__} {self.animal.nome} por {self.adotante.nome} em {self.data.day}/{self.data.month}/{self.data.year}"

    def __repr__(self) -> str:
        return f"Adocao(id={self.id}, animal={repr(self.animal)}, adotante={repr(self.adotante)}, taxa={self.taxa}, pago={self.pago}, data={self.data})"

class Devolucao(Registro):
    """Classe para modelar devoluções no sistema

    A classe herda atributos de Registro e também possui os próprios
    atributos.

    Attributes:
        motivo (COMPORTAMENTO, PESSOAL, DOENCA, OUTRO): Tipo do motivo
        data (date): Data da devolução.
    """

    def __init__(
        self,
        *,
        id: int,
        animal: Animal,
        adotante: Adotante,
        motivo: str,
        data: datetime,
    ):
        super().__init__(id=id, animal=animal, adotante=adotante)
        self.motivo: MotivoDevolucao = motivo  # property setter (privado)
        self.data: datetime = data

    @property
    def motivo(self) -> str:
        return self.__motivo.value

    @motivo.setter
    def motivo(self, motivo: str) -> None:
        try:
            if isinstance(MotivoDevolucao(motivo), MotivoDevolucao):
                self.__motivo = MotivoDevolucao(motivo)
        except ValueError:
            raise TipagemError("MotivoDevolucao", motivo)

    def __str__(self) -> str:
        return f"Devolução de {type(self.animal).__name__} {self.animal.nome} por {self.adotante.nome} em {self.data.day}/{self.data.month}/{self.data.year} por motivo de {self.motivo}"

    def __repr__(self) -> str:
        return f"Adocao(id={self.id}, animal={repr(self.animal)}, adotante={repr(self.adotante)}, motivo={self.motivo}, data={self.data})"