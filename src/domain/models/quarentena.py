from src.domain.enums import MotivoQuarentena, StatusQuarentena
from src.domain.exceptions import TipagemError

from datetime import datetime


class Quarentena:
    """Classe para modelar quarentenas no sistema.

    A classe não possui relacionamantos de herança.

    Attibutes:
        animal (id - Animal): Id do animal envolvido.
        data_inicial (date): Data inicial da quarentena.
        data_final (null | date): Data final da quarentena.
        motivo (COMPORTAMENTO, DOENCA, OUTRO): Motivo da quarentena.
        status (ATIVA, CUMPRIDA): Status da quarentena.
    """

    def __init__(
        self,
        *,
        animal: int,
        data_inicial: datetime,
        data_final: datetime | None = None,
        motivo: str,
        status: str,
    ):
        self.__animal: int = animal  # não pode ser alterado, apenas lido
        self.data_inicial: datetime = data_inicial
        self.data_final: datetime | None = data_final
        self.motivo: MotivoQuarentena = motivo  # property setter (privado)
        self.status: StatusQuarentena = status  # property setter (privado)

    # __animal: apenas getter
    @property
    def animal(self) -> int:
        return self.__animal

    # __motivo: possui getter e setter para validação de tipagem
    @property
    def motivo(self) -> str:
        return self.__motivo.value

    @motivo.setter
    def motivo(self, motivo: str) -> None:
        try:
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
            if isinstance(StatusQuarentena(status), StatusQuarentena):
                self.__status = StatusQuarentena(status)
        except ValueError:
            raise TipagemError("StatusQuarentena", status)
