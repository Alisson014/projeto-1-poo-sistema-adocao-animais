from src.domain.enums import TipoEvento
from src.domain.exceptions import TipagemError

from datetime import datetime


class Evento:
    """Classe auxiliar para modelar os eventos.

    A classe modela os eventos que podem ser registrados no histórico de um
    animal. Será utilizada em conjunto com a classe animal.

    Attributes:
        tipo (VACINA, ADOCAO, DEVOLUCAO, QUARENTENA, CONSULTA): Tipo do evento.
        descricao (string): Descrição do evento.
        data (date): Data de ocorrência do evento.
    """

    def __init__(self, *, tipo: str, descricao: str, data: datetime):
        self.tipo: TipoEvento = tipo  # property setter (privado)
        self.descricao: str = descricao
        self.data: datetime = data

    # __tipo possui getter e setter para garantir validação da tipagem
    @property
    def tipo(self):
        return self.__tipo.value

    @tipo.setter
    def tipo(self, tipo: str):
        try:
            # Se não for válido, essa verificação dispara um erro
            # Evitando que o estado seja alterado
            if isinstance(TipoEvento(tipo), TipoEvento):
                # Valida se a string é um TipoEvento válido
                self.__tipo = TipoEvento(tipo)
        except ValueError:
            raise TipagemError("TipoEvento", tipo)

    def __str__(self) -> str:
        return f"Evento de {self.tipo}, {self.data} {self.descricao}"

    def __repr__(self) -> str:
        return f"Evento(tipo={self.tipo}, data={self.data} descricao={self.descricao})"

    def __eq__(self, outro_evento) -> bool:
        return repr(self) == repr(outro_evento)


class Vacina:
    """Classe para modelar vacinas.

    A classe modela as vacinas adicionadas na agenda de vacinas de animais
    vacináveis. Será utilizada em conjunto com a classe VacinavelMixin.

    Attributes:
        nome (string): Nome da vacina.
        data (datetime): Data de aplicação.
    """

    def __init__(self, *, nome: str, data: datetime):
        self.nome: str = nome
        self.data: datetime = data

    def __str__(self) -> str:
        return f"Vacina {self.nome} aplicada em {self.data.day}/{self.data.month}/{self.data.year}"

    def __repr__(self) -> str:
        return f"Vacina(nome={self.nome}, data={self.data})"

    def __eq__(self, outro_evento) -> bool:
        return repr(self) == repr(outro_evento)
