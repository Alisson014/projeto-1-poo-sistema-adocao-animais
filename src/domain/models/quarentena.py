from src.domain.enums import MotivoQuarentena, StatusQuarentena
from .animal import Animal, Cachorro, Calopsita, Coelho, Gato
from src.domain.exceptions import TipagemError

from datetime import datetime


class Quarentena:
    """Classe para modelar quarentenas no sistema.

    A classe não possui relacionamantos de herança.

    Attibutes:
        animal (Animal): Animal envolvido.
        data_inicial (date): Data inicial da quarentena.
        data_final (null | date): Data final da quarentena.
        motivo (COMPORTAMENTO, DOENCA, OUTRO): Motivo da quarentena.
        status (ATIVA, CUMPRIDA): Status da quarentena.
    """

    def __init__(
        self,
        *,
        id: int,
        animal: Animal,
        data_inicial: datetime,
        data_final: datetime | None = None,
        motivo: str,
        status: str,
    ):
        self.__id = int(id) # não pode ser alterado, apenas lido
        self.__animal: Animal | Cachorro | Calopsita | Coelho | Gato = animal  # não pode ser alterado, apenas lido
        self.data_inicial: datetime = datetime.fromisoformat(data_inicial) if isinstance(data_inicial, str) else data_inicial
        self.data_final: datetime | None = datetime.fromisoformat(data_final) if isinstance(data_final, str) else data_final
        self.motivo: MotivoQuarentena = motivo  # property setter (privado)
        self.status: StatusQuarentena = status  # property setter (privado)

    # __id: apenas getter
    @property
    def id(self):
        return self.__id

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

    @classmethod
    def from_dict(cls, quarentena:dict):

        return cls(**quarentena)

    def to_dict(self):
        return {
            "id": self.id,
            "animal": self.animal.id,
            "data_inicial": self.data_inicial.__str__(),
            "data_final": self.data_final.__str__() if self.data_final else None,
            "motivo": self.motivo,
            "status": self.status,
        }

    def __str__(self) -> str:
        return f"Quarentena do animal {self.animal.__str__()} iniciada em {self.data_inicial.day}/{self.data_inicial.month}{self.data_inicial.year}, por {self.motivo}. Está {self.status}"

    def __repr__(self) -> str:
        return f"Quarentena(animal={repr(self.animal)}, data_inicial={self.data_inicial}, data_final={self.data_final}, motivo={self.motivo}, status={self.status})"
