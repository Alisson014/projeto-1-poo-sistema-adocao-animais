from src.config import PesosCompatibilidade
from src.domain.models.pessoa import Adotante
from src.domain.models.animal import Animal
from src.domain.exceptions import TipagemError, NaoEncontradoError
from src.utils import get_compatibilidade

from datetime import datetime, timedelta

class EntradaFila:
    """Classe para modelar entradas na fila de espera.

    A classe modela as entradas que serão armazenadas na
    fina de espera de um animal. Será utilizada em conjunto com a classe FilaEspera.

    Attributes:
        adotante (Adotante): Adotante considerado.
        data_inicial (datetime): Data de início da entrada
        data_expiracao (datetime): Data final da entrada
        compatibilidade (float): nível de compatibilidade entre o adotante e o animal considerado.
    """

    def __init__(
        self, *, adotante: Adotante, compatibilidade: float, data_expiracao: datetime | str, data_inicial: datetime | str = datetime.now()
    ):
        self.__adotante: Adotante = adotante  # Pode ser apenas lido via property getter
        self.data_expiracao = datetime.fromisoformat(data_expiracao) if isinstance(data_expiracao, str) else data_expiracao
        self.data_inicial = datetime.fromisoformat(data_inicial) if isinstance(data_inicial, str) else data_inicial
        # Pode ser apenas lido via property getter
        self.__compatibilidade: float = compatibilidade

    # __adotante não pode ser alterado
    @property
    def adotante(self):
        return self.__adotante

    # __compatibilidade não pode ser alterada
    @property
    def compatibilidade(self):
        return self.__compatibilidade

    @classmethod
    def from_dict(cls, entrada:dict):
        return cls(**entrada)

    def to_dict(self):
        return {
            "adotante":self.adotante.email,
            "compatibilidade": self.compatibilidade,
            "data_inicial": self.data_inicial.__str__(),
            "data_expiracao": self.data_expiracao.__str__()
        }

    def __str__(self) -> str:
        return f"Entrada para espera de {self.adotante.nome}, compatibilidade({self.compatibilidade})"

    def __repr__(self) -> str:
        return f"EntradaFila(adotante={repr(self.adotante)}, compatibilidade={self.compatibilidade}, data_inicial={self.data_inicial}, data_expiracao={self.data_expiracao})"

    def __eq__(self, outra_entrada: object) -> bool:
        if not isinstance(outra_entrada, EntradaFila):
            return NotImplemented
        return repr(self) == repr(outra_entrada)

    def __lt__(self, outra_entrada) -> bool:
        if not isinstance(outra_entrada, EntradaFila):
            return NotImplemented
        return self.compatibilidade < outra_entrada.compatibilidade


class FilaEspera:
    """Classe para modelar filas de espera no sistema

    A classe não possui herança e armazena uma lista de objetos
    da classe EntradaFila.

    Attributes:
        animal (id - Animal): Id do animal da fila de espera.
        duracao_reserva (int): Duracao máxima em dias
        fila (List[EntradaFila]): Lista de entradas com interesse no animal.
    """

    def __init__(self, *, animal: Animal, duracao_reserva:int, pesos:PesosCompatibilidade, fila: list | None = None):
        self.__animal: Animal = animal  # Pode ser apenas lido via getter
        self.fila: list[EntradaFila] = fila if fila is not None else []
        self.duracao_reserva = duracao_reserva
        self.pesos:PesosCompatibilidade = pesos

    # __animal não pode ser alterado
    @property
    def animal(self):
        return self.__animal

    @classmethod
    def from_dict(cls, fila:dict):
        return cls(**fila)

    def to_dict(self):
        return {
            "animal": self.animal.id,
            "duracao_reserva": self.duracao_reserva,
            "fila": self.get_fila()
        }

    # Métodos
    def add(self, adotante: Adotante) -> None:
        """Adiciona um adotante à fila de espera"""
        
        if not isinstance(adotante, Adotante): 
            raise TipagemError("Adotante", adotante)

        for entr in self.fila:
            if entr.adotante == adotante:
                raise Exception("Um adotante não pode estar na mesma fila duas vezes")

        # Cria a entrada e adiciona na fila
        entrada = EntradaFila(adotante=adotante, compatibilidade=get_compatibilidade(self.animal, adotante, self.pesos), data_inicial=datetime.now(), data_expiracao=datetime.now() + timedelta(days=self.duracao_reserva))
        
        is_last = True
        for i, ent in enumerate(self.fila):
            if ent.compatibilidade < entrada.compatibilidade:
                self.fila.insert(i, entrada)
                is_last = False
                break

        if is_last:
            self.fila.append(entrada)


    def remove(self, adotante: Adotante):
        """Remove um adotante da fila de espera"""
        
        if not isinstance(adotante, Adotante): 
            raise TipagemError("Adotante", adotante)
        

        for i, e in enumerate(self.fila):
            # Busca o adotante comparando os emails
            # Posso implementar isso via __eq__
            if e.adotante == adotante:
                self.fila.pop(i)
                return

        raise NaoEncontradoError("Adotante")

    def proximo(self) -> EntradaFila | None:
        """Retorna o próximo adotante na fila de espera"""
        # Posso implementar o __len__ aqui
        if len(self.fila) == 0:
            # Retorna None se a fila estiver vazia
            return None

        # retorna sempre o primeiro
        return self.fila[0]

    def get_fila(self) -> list[dict]:
        """Retorna uma lista de emails das entradas da fila"""
        res = []

        for en in self.fila:
            res.append(en.to_dict())

        return res

    def __str__(self) -> str:
        return f"Fila de Espera do animal {self.animal.nome}"

    def __repr__(self) -> str:
        return f"FilaEspera(animal={repr(self.animal)}, fila={self.fila})"

    def __len__(self) -> int:
        return len(self.fila)

    def __contains__(self, item) -> bool:
        if not isinstance(item, EntradaFila):
            return False

        for i in self.fila:
            # Compara via __eq__ de EntradaFila
            if i == item:
                return True

        return False

    def __lt__(self, outra_fila) -> bool:
        if not isinstance(outra_fila, FilaEspera):
            return NotImplemented
        return len(self) < len(outra_fila)
