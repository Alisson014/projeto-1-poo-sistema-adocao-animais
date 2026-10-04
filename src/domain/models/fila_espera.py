from src.domain.models.pessoa import Adotante
from src.domain.exceptions import TipagemError, NaoEncontradoError


class EntradaFila:
    """Classe para modelar entradas na fila de espera.

    A classe modela as entradas que serão armazenadas na
    fina de espera de um animal. Será utilizada em conjunto com a classe FilaEspera.

    Attributes:
        adotante (id - Adotante): id do adotante considerado.
        tempo_espera (int): tempo de espera em dias.
        compatibilidade (float): nível de compatibilidade entre o adotante e o animal considerado.
    """

    def __init__(self, *, adotante: dict, tempo_espera: int, compatibilidade: float):
        self.__adotante: dict = adotante  # Pode ser apenas lido via property getter
        self.tempo_espera: int = tempo_espera
        self.__compatibilidade: float = (
            compatibilidade  # Pode ser apenas lido via property getter
        )

    @property
    def adotante(self):
        return self.__adotante

    @property
    def compatibilidade(self):
        return self.__compatibilidade


class FilaEspera:
    """Classe para modelar filas de espera no sistema

    A classe não possui herança e armazena uma lista de objetos
    da classe EntradaFila.

    Attributes:
        animal (id - Animal): Id do animal da fila de espera.
        fila (List[EntradaFila]): Lista de entradas com interesse no animal.
    """

    def __init__(self, *, animal: int, fila: list[EntradaFila] = []):
        self.__animal: int = animal  # Pode ser apenas lido via getter
        self.__fila = fila

    @property
    def animal(self):
        return self.__animal

    # Métodos
    def add(self, adotante: Adotante) -> None:
        """Adiciona um adotante à fila de espera"""
        if not isinstance(adotante, Adotante):
            raise TipagemError("Adotante", adotante)

        entrada = EntradaFila(
            adotante=adotante.__dict__, tempo_espera=0, compatibilidade=100
        )
        self.__fila.append(entrada)

        ##### Precisa inserir ordenando pelo nível de compatibilidade
        ##### Só posso aplicar isso depois de implementar os strategy e as políticas

    def remove(self, adotante: Adotante):
        """Remove um adotante da fila de espera"""
        if not isinstance(adotante, Adotante):
            raise TipagemError("Adotante", adotante)

        for i, e in enumerate(self.__fila):
            print(e.adotante["_Pessoa__email"])
            print(adotante.email)
            if e.adotante["_Pessoa__email"] == adotante.email:
                self.__fila.pop(i)
                return

        raise NaoEncontradoError("Adotante")

    def proximo(self) -> EntradaFila | None:
        """Retorna o próximo adotante na fila de espera"""
        if len(self.__fila) == 0:
            # Retorna None se a fila estiver vazia
            return None

        # retorna sempre o primeiro
        return self.__fila[0]

    def get_fila(self):
        """Retorna uma lista de dicionárias das entradas"""
        res = []

        for en in self.__fila:
            res.append(en.__dict__)

        return res
