from src.domain.models.pessoa import Adotante
from src.domain.models.animal import Animal
from src.domain.exceptions import TipagemError, NaoEncontradoError


class EntradaFila:
    """Classe para modelar entradas na fila de espera.

    A classe modela as entradas que serão armazenadas na
    fina de espera de um animal. Será utilizada em conjunto com a classe FilaEspera.

    Attributes:
        adotante (Adotante): Adotante considerado.
        tempo_espera (int): tempo de espera em dias.
        compatibilidade (float): nível de compatibilidade entre o adotante e o animal considerado.
    """

    def __init__(
        self, *, adotante: Adotante, tempo_espera: int, compatibilidade: float
    ):
        self.__adotante: Adotante = adotante  # Pode ser apenas lido via property getter
        self.tempo_espera: int = tempo_espera
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

    def __str__(self) -> str:
        return f"Entrada para espera de {self.adotante.nome}, tempo de espera de {self.tempo_espera} e compatibilidade({self.compatibilidade})"

    def __repr__(self) -> str:
        return f"EntradaFila(adotante={repr(self.adotante)}, tempo_espera={self.tempo_espera}, compatibilidade={self.compatibilidade})"

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
        fila (List[EntradaFila]): Lista de entradas com interesse no animal.
    """

    def __init__(self, *, animal: Animal, fila: list[EntradaFila] = []):
        self.__animal: Animal = animal  # Pode ser apenas lido via getter
        self.__fila = fila

    # __animal não pode ser alterado
    @property
    def animal(self):
        return self.__animal

    # Métodos
    def add(self, adotante: Adotante) -> None:
        """Adiciona um adotante à fila de espera"""
        try:
            # Valida a tipagem de adotante
            # Se não for dispara um erro
            isinstance(adotante, Adotante)
        except ValueError:
            raise TipagemError("Adotante", adotante)

        # Cria a entrada e adiciona na fila
        entrada = EntradaFila(adotante=adotante, tempo_espera=0, compatibilidade=100)
        self.__fila.append(entrada)

        ##### Precisa inserir ordenando pelo nível de compatibilidade
        ##### Só posso aplicar isso depois de implementar os strategy e as políticas

    def remove(self, adotante: Adotante):
        """Remove um adotante da fila de espera"""
        try:
            # Valida a tipagem de adotante
            # Se não for dispara um erro
            isinstance(adotante, Adotante)
        except ValueError:
            raise TipagemError("Adotante", adotante)

        for i, e in enumerate(self.__fila):
            # Busca o adotante comparando os emails
            # Posso implementar isso via __eq__
            if e.adotante == adotante:
                self.__fila.pop(i)
                return

        raise NaoEncontradoError("Adotante")

    def proximo(self) -> EntradaFila | None:
        """Retorna o próximo adotante na fila de espera"""
        # Posso implementar o __len__ aqui
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

    def __str__(self) -> str:
        return f"Fila de Espera do animal {self.animal.nome}"

    def __repr__(self) -> str:
        return f"FilaEspera(animal={repr(self.animal)}, fila={self.__fila})"

    def __len__(self) -> int:
        return len(self.__fila)

    def __contains__(self, item) -> bool:
        if not isinstance(item, EntradaFila):
            return NotImplemented

        for i in self.__fila:
            # Compara via __eq__ de EntradaFila
            if i == item:
                return True

        return False

    def __lt__(self, outra_fila) -> bool:
        if not isinstance(outra_fila, FilaEspera):
            return NotImplemented
        return len(self) < len(outra_fila)
