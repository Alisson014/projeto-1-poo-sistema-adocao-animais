from src.domain.models.animal import Animal, Cachorro, Calopsita, Coelho, Gato
from src.domain.models.pessoa import Adotante
from src.domain.models.registro import Adocao, Devolucao
from src.domain.enums import Porte
from src.domain.exceptions import RelatorioNaoGeradoError

from abc import ABC, abstractmethod
from datetime import datetime

def adocao_serializer(adocao:Adocao):
    return {
        "id": adocao.id,
        "animal": adocao.animal.to_dict(),
        "adotante": adocao.adotante.to_dict(),
        "taxa": adocao.taxa,
        "pago": adocao.pago,
        "data": adocao.data.__str__()
    }

def devolucao_serializer(adocao:Devolucao):
    return {
        "id": adocao.id,
        "animal": adocao.animal.to_dict(),
        "adotante": adocao.adotante.to_dict(),
        "motivo": adocao.motivo,
        "data": adocao.data.__str__()
    }

def get_dict_list(array: list):
    """Método auxiliar que retorna uma lista de dicionários de uma lista de objetos"""
    dict_list = []

    for i in array:
        if isinstance(i, Adocao):
            dict_list.append(adocao_serializer(i))
        elif isinstance(i, Devolucao):
            dict_list.append(devolucao_serializer(i))
        else:
            dict_list.append(i.to_dict())

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
        top5: list[Animal]=[]
    ):
        super().__init__(id=id, data=data, nome=nome)
        self.animais = animais
        self.adotantes = adotantes
        self.top5: list[Animal] = top5

    @classmethod
    def from_dict(cls, relatorio:dict):
        return cls(**relatorio)

    def gerar(self):
        """Gera uma lista com os dicionários contendo os 5 animais mais adotáveis ordenados pela média de compatibilidade"""
        # Só pode ser desenvolvido quando eu definir o cálculo de compatibilidade
        # Por hora, esta classe é apenas simulada
        # Considerando os primeiros 5 animais
        for i in self.animais:
            self.top5.append(i)
            if len(self.top5) >= 5:
                break

    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if not self.top5:
            raise RelatorioNaoGeradoError()

        # Retorna um dicionário com as informações
        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data.__str__(),
            "animais": get_dict_list(self.animais),
            "adotantes": get_dict_list(self.adotantes),
            "top5": get_dict_list(self.top5),
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

    def __init__(self, *, id: int, data: datetime, nome: str, adocoes: list[Adocao], taxas={}):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.taxas: dict[str, str] = taxas

    @classmethod
    def from_dict(cls, relatorio:dict):
        return cls(**relatorio)

    def gerar(self):
        """Gere um dicionário que armazena os pares de chave e valor {"Animal": "adotados/Total"}
        referentes as taxas de adoção de cada Animal no sistema"""

        # Dicionário para mapear a quantidade de cada animal
        totais = {
            "Cachorro": 0,
            "Calopsita": 0,
            "Coelho": 0,
            "Gato": 0,
        }

        # Contagem via tipagem dos animais na lista
        for a in self.adocoes:
            totais[type(a.animal).__name__] += 1

        total_adocoes = len(self.adocoes)

        # Armazenando os dados no atributo
        self.taxas = {
            "Cachorro": f"{totais["Cachorro"]}/{total_adocoes}",
            "Calopsita": f"{totais["Calopsita"]}/{total_adocoes}",
            "Coelho": f"{totais["Coelho"]}/{total_adocoes}",
            "Gato": f"{totais["Gato"]}/{total_adocoes}",
        }

    def exportar(self) -> dict:
        """Retorna um relatório estruturado como dicionário"""
        if not self.taxas:
            raise RelatorioNaoGeradoError()

        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data.__str__(),
            "adocoes": get_dict_list(self.adocoes),
            "taxas": self.taxas,
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

    def __init__(self, *, id: int, data: datetime, nome: str, adocoes: list[Adocao], taxas={}):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.taxas: dict[str, str] = taxas

    @classmethod
    def from_dict(cls, relatorio:dict):
        return cls(**relatorio)

    def gerar(self):
        """Gere um dicionário que armazena os pares de chave e valor {"Animal": "adotados/Total"}
        referentes as taxas de adoção de cada Animal no sistema"""
        # Dicionário para mapear os portes e suas quantidades
        totais = {Porte.P.value: 0, Porte.M.value: 0, Porte.G.value: 0}

        # Contagem via porte do animal na lista
        for a in self.adocoes:
            totais[a.animal.porte] += 1

        total_adocoes = len(self.adocoes)

        self.taxas = {
            Porte.P.value: f"{totais[Porte.P.value]}/{total_adocoes}",
            Porte.M.value: f"{totais[Porte.M.value]}/{total_adocoes}",
            Porte.G.value: f"{totais[Porte.G.value]}/{total_adocoes}",
        }

    def exportar(self) -> dict:
        """Retorna um relatório estruturado como dicionário"""
        if not self.taxas:
            raise RelatorioNaoGeradoError()

        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data.__str__(),
            "adocoes": get_dict_list(self.adocoes),
            "taxas": self.taxas,
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

    def __init__(self, *, id: int, data: datetime, nome: str, adocoes: list[Adocao], tempo_medio_meses=None):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.tempo_medio_meses: int | None = tempo_medio_meses

    @classmethod
    def from_dict(cls, relatorio:dict):
        return cls(**relatorio)

    def gerar(self):
        """Gera o tempo média entre entrada e adoção dos adotados"""
        # Armazena a soma dos tempos entre a entrada e a adoção
        soma = 0
        for a in self.adocoes:
            soma += (a.data.year - a.animal.data_entrada.year) * 12 + (
                a.data.month - a.animal.data_entrada.month
            )
            if a.data.day < a.animal.data_entrada.day:
                soma -= 1

        # Divide pela quantidade para obter o tempo médio
        total_adocoes = len(self.adocoes)
        if total_adocoes != 0:
            self.tempo_medio_meses = soma / total_adocoes
        else:
            self.tempo_medio_meses = 0

    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if self.tempo_medio_meses is None:
            raise RelatorioNaoGeradoError()

        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data.__str__(),
            "adocoes": get_dict_list(self.adocoes),
            "tempo_medio_meses": self.tempo_medio_meses,
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
        taxa = ""
    ):
        super().__init__(id=id, data=data, nome=nome)
        self.adocoes: list[Adocao] = adocoes
        self.devolucoes: list[Devolucao] = devolucoes
        self.taxa: str = taxa

    @classmethod
    def from_dict(cls, relatorio:dict):
        return cls(**relatorio)

    def gerar(self):
        """Calcula a taxa de devoluções por adoção"""
        self.taxa = f"{((len(self.devolucoes) / len(self.adocoes)) * 100):.2f}%"

    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if not self.taxa:
            raise RelatorioNaoGeradoError()

        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data.__str__(),
            "adocoes": get_dict_list(self.adocoes),
            "devolucoes": get_dict_list(self.devolucoes),
            "taxa": self.taxa,
        }

    def __str__(self) -> str:
        return f"Relatório da taxa de devoluções"
