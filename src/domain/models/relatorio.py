from src.domain.models.animal import Animal, Cachorro, Calopsita, Coelho, Gato
from src.domain.models.pessoa import Adotante
from src.domain.models.registro import Adocao, Devolucao
from src.domain.enums import Porte
from src.domain.exceptions import RelatorioNaoGeradoError

from abc import ABC, abstractmethod
from datetime import datetime


def get_dict_list(array: list):
    """Método auxiliar que retorna uma lista de dicionários de uma lista de objetos"""
    dict_list = []
    for i in array:
        dict_list.append(i.__dict__)

    return dict_list


class Relatorio(ABC):
    """Classe abstrata para modelar relatorios no sistema.

    A classe define os atributos e métodos comuns a todos os relatórios
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        id (int): Identificador único do relatório.
        data (date): Data de criação do relatório.
        nome (string): Nome do relatório.
    """

    def __init__(self, *, id: int, data: datetime, nome: str):
        self.__id: int = id  # Pode ser apenas lido
        self.data: datetime = data
        self.nome = nome

    @property
    def id(self) -> int:
        return self.__id

    @abstractmethod
    def gerar(self):
        pass

    @abstractmethod
    def exportar(self):
        pass


class Top5MaisAdotaveis(Relatorio):
    """Classe para modelar relatórios de animais mais adotáveis

    A classe herda atributos de Relatório e também possui os próprios
    atributos específicos.

    Attributes:
        animais (List[Animal]): Lista de animais considerada no momento da criação.
        adotantes (List[Adotante]): Lista de adotantes considerada no momento da criação.
        top5 (List[Animal]): Lista dos 5 animais mais adotáveis.
    """

    def __init__(
        self,
        *,
        id: int,
        data: datetime,
        nome: str,
        animais: list[Animal],
        adotantes: list[Adotante],
    ):
        super().__init__(id=id, data=data, nome=nome)
        self.animais = animais
        self.adotantes = adotantes
        self.__top5: list[dict] = []

    def gerar(self):
        """Gera uma lista com os dicionários contendo os 5 animais mais adotáveis ordenados pela média de compatibilidade"""
        # Só pode ser desenvolvido quando eu definir o cálculo de compatibilidade

    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if not self.__top5:
            raise RelatorioNaoGeradoError()

        return {
            "nome": self.nome,
            "animais": get_dict_list(self.animais),
            "adotantes": get_dict_list(self.adotantes),
            "top5": self.__top5,
        }

    def __str__(self) -> str:
        return f"Relatório dos 5 animais mais adotáveis"


class TaxaAdocaoEspecies(Relatorio):
    """Classe para modelar os relatórios com as taxas de adoção por Animais.

    A classe herda atributos de Relatório e também possui os próprios
    atributos específicos.

    Attributes:
        adocoes (List[Adocao]): Lista das adoções consideradas;
        taxas (dict): Dicionário que armazena os pares de chave e valor {"Animal": "adotados/Total"}
    """

    def __init__(self, *, id: int, data: datetime, nome: str, adocoes: list[Adocao]):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.__taxas: dict[str, str] = {}

    def gerar(self):
        """Gere um dicionário que armazena os pares de chave e valor {"Animal": "adotados/Total"}
        referentes as taxas de adoção de cada Animal no sistema"""
        totais = {
            type(Cachorro).__name__: 0,
            type(Calopsita).__name__: 0,
            type(Coelho).__name__: 0,
            type(Gato).__name__: 0,
        }
        for a in self.adocoes:
            totais[type(a.animal).__name__] += 1

        total_adocoes = len(self.adocoes)

        self.__taxas = {
            type(
                Cachorro
            ).__name__: f"{totais[type(Cachorro).__name__]}/{total_adocoes}",
            type(
                Calopsita
            ).__name__: f"{totais[type(Calopsita).__name__]}/{total_adocoes}",
            type(Coelho).__name__: f"{totais[type(Coelho).__name__]}/{total_adocoes}",
            type(Gato).__name__: f"{totais[type(Gato).__name__]}/{total_adocoes}",
        }

    def exportar(self) -> dict:
        """Retorna um relatório estruturado como dicionário"""
        if not self.__taxas:
            raise RelatorioNaoGeradoError()

        return {
            "nome": self.nome,
            "adocoes": get_dict_list(self.adocoes),
            "taxas": self.__taxas,
        }

    def __str__(self) -> str:
        return f"Relatório da Taxa de Adoção por espécies"


class TaxaAdocaoPorte(Relatorio):
    """Classe para modelar os relatórios com as taxas de adoção por portes.

    A classe herda atributos de Relatório e também possui os próprios
    atributos específicos.

    Attributes:
        adocoes (List[Adocao]): Lista das adoções consideradas;
        taxas (dict): Dicionário que armazenas os pares de chave e valor {"Porte": "adotados/Total"}
    """

    def __init__(self, *, id: int, data: datetime, nome: str, adocoes: list[Adocao]):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.__taxas: dict[str, str] = {}

    def gerar(self):
        """Gere um dicionário que armazena os pares de chave e valor {"Animal": "adotados/Total"}
        referentes as taxas de adoção de cada Animal no sistema"""
        totais = {Porte.P.value: 0, Porte.M.value: 0, Porte.G.value: 0}
        for a in self.adocoes:
            totais[a.animal.porte] += 1

        total_adocoes = len(self.adocoes)

        self.__taxas = {
            Porte.P.value: f"{totais[Porte.P.value]}/{total_adocoes}",
            Porte.M.value: f"{totais[Porte.M.value]}/{total_adocoes}",
            Porte.G.value: f"{totais[Porte.G.value]}/{total_adocoes}",
        }

    def exportar(self) -> dict:
        """Retorna um relatório estruturado como dicionário"""
        if not self.__taxas:
            raise RelatorioNaoGeradoError()

        return {
            "nome": self.nome,
            "adocoes": get_dict_list(self.adocoes),
            "taxas": self.__taxas,
        }

    def __str__(self) -> str:
        return f"Relatório da taxa de adoção por portes"

class TaxaTempoMedioEntradaAdocao(Relatorio):
    """Classe para modelar os relatórios com o tempo médio entre entrada e adoção.

    A classe herda atributos de Relatório e também possui os próprios
    atributos específicos.

    Attributes:
        adocoes (List[Adocao]): Adoções consideradas no relatório.
        tempo_medio_meses (int): Tempo médio em meses.
    """

    def __init__(self, *, id: int, data: datetime, nome: str, adocoes: list[Adocao]):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.__tempo_media_meses: int = 0

    def gerar(self):
        """Gera o tempo média entre entrada e adoção dos adotados"""
        soma = 0
        for a in self.adocoes:
            soma += (a.data.year - a.animal.data_entrada.year) * 12 + (
                a.data.month - a.animal.data_entrada.month
            )
            if a.data.day < a.animal.data_entrada.day:
                soma -= 1

        self.__tempo_media_meses = soma / len(self.adocoes)

    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if not self.__tempo_media_meses:
            raise RelatorioNaoGeradoError()

        return {
            "nome": self.nome,
            "adocoes": get_dict_list(self.adocoes),
            "tempo_medio_meses": self.__tempo_media_meses,
        }

    def __str__(self) -> str:
        return f"Relatório do tempo médio entre entrada e adoção"

class TaxaDevolucoes(Relatorio):
    """Classe para modelar os relatórios com a taxa entre adoções e devoluções;

    A classe herda atributos de Relatório e também possui os próprios
    atributos específicos.

    Attributes:
        adocoes (List[Adocao]): Lista de adoções considerada.
        devolucoes (List[Devolucao]): Lista de devoluções considerada.
        taxa (string): Taxa de devoluções por Adoções
    """

    def __init__(
        self,
        *,
        id: int,
        data: datetime,
        nome: str,
        adocoes: list[Adocao],
        devolucoes: list[Devolucao],
    ):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.devolucoes: list[Devolucao] = devolucoes
        self.__taxa: str = ""

    def gerar(self):
        """Calcula a taxa de devoluções por adoção"""
        self.__taxa = f"{((len(self.devolucoes) / len(self.adocoes)) * 100):.2f}%"

    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if not self.__taxa:
            raise RelatorioNaoGeradoError()

        return {
            "nome": self.nome,
            "adocoes": get_dict_list(self.adocoes),
            "devolucoes": get_dict_list(self.devolucoes),
            "taxa": self.__taxa,
        }

    def __str__(self) -> str:
        return f"Relatório da taxa de devoluções"
