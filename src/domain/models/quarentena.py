from src.domain.enums import MotivoQuarentena, StatusQuarentena
from .animal import Animal
from src.domain.exceptions import TipagemError

from datetime import datetime


class Quarentena:
    """Classe para modelar quarentenas no sistema.

    A classe não possui relacionamantos de herança.

    Attibutes:
        animal Animal: Animal envolvido.
        data_inicial (date): Data inicial da quarentena.
        data_final (null | date): Data final da quarentena.
        motivo (COMPORTAMENTO, DOENCA, OUTRO): Motivo da quarentena.
        status (ATIVA, CUMPRIDA): Status da quarentena.
    """

    def __init__(
        self,
        *,
        animal: Animal,
        data_inicial: datetime,
        data_final: datetime | None = None,
        motivo: str,
        status: str,
    ):
        self.__animal: Animal = animal  # não pode ser alterado, apenas lido
        self.data_inicial: datetime = data_inicial
        self.data_final: datetime | None = data_final
        self.motivo: MotivoQuarentena = motivo  # property setter (privado)
        self.status: StatusQuarentena = status  # property setter (privado)

    # __animal: apenas getter
    @property
    def animal(self):
        return self.__animal

    # __motivo: possui getter e setter para validação de tipagem
    @property
    def motivo(self) -> str:
        return self.__motivo.value

    @motivo.setter
    def motivo(self, motivo: str) -> None:
        try:
            # Se não for válido, essa verificação dispara um erro
            # Evitando que o atributo seja alterado
            if isinstance(MotivoQuarentena(motivo), MotivoQuarentena):
                self.__motivo = MotivoQuarentena(motivo)
        except ValueError:
            raise TipagemError("MotivoQuarentena", motivo)

    # __motivo: possui getter e setter para validação de tipagem
    @property
    def status(self) -> str:
        return self.__status.value

    @status.setter
    def status(self, status: str) -> None:
        try:
            # Se não for válido, essa verificação dispara um erro
            # Evitando que o atributo seja alterado
            if isinstance(StatusQuarentena(status), StatusQuarentena):
                self.__status = StatusQuarentena(status)
        except ValueError:
            raise TipagemError("StatusQuarentena", status)

    def __str__(self) -> str:
        return f"Quarentena do animal {self.animal.__str__()} iniciada em {self.data_inicial.day}/{self.data_inicial.month}{self.data_inicial.year}, por {self.motivo}. Está {self.status}"

    def __repr__(self) -> str:
        return f"Quarentena(animal={repr(self.animal)}, data_inicial={self.data_inicial}, data_final={self.data_final}, motivo={self.motivo}, status={self.status})"