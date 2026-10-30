from src.domain.models.animal import Animal, Cachorro, Calopsita, Coelho, Gato
from src.domain.models.pessoa import Adotante
from src.domain.models.registro import Adocao, Devolucao
from src.domain.enums import Porte
from src.domain.exceptions import RelatorioNaoGeradoError
from src.config import PesosCompatibilidade
from src.utils import get_compatibilidade, adocao_serializer, devolucao_serializer

from abc import ABC, abstractmethod
from datetime import datetime

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
        self.data: datetime = datetime.fromisoformat(data) if isinstance(data, str) else data
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
        pesos_compatibilidade (PesosCompatibilidade): Os pesos utilizados no cálculo de compatibilidade
    """

    def __init__(
        self,
        *,
        id: int,
        data: datetime,
        nome: str,
        animais: list[Animal],
        adotantes: list[Adotante],
        top5: list[Animal] | None = None,
        pesos_compatibilidade: PesosCompatibilidade | None = None
    ):
        super().__init__(id=id, data=data, nome=nome)
        self.animais = animais
        self.adotantes = adotantes
        self.top5: list[Animal] = top5 if top5 is not None else []
        self.pesos_compatibilidade = pesos_compatibilidade

    @classmethod
    def from_dict(cls, relatorio:dict):
        return cls(**relatorio)

    def gerar(self):
        """Gera uma lista contendo os 5 animais mais adotáveis ordenados pela média de compatibilidade"""
        if self.pesos_compatibilidade is None:
            raise Exception("Não há pesos para fazer a verificação")

        self.top5 = []

        if not self.adotantes or not self.animais:
            return self.top5

        # Como a compatibilidade de um animal jamais será negativa
        # O -1 é utilizado como controle
        hank:list[tuple[float, Animal | None]] = [ 
            (-1, None ),
            (-1, None ),
            (-1, None ),
            (-1, None ),
            (-1, None )
        ]
        
        for animal in self.animais:
            # Cálculo da compatibilidade média
            comp_media = 0
            for adotante in self.adotantes:
                comp_media += get_compatibilidade(animal, adotante, self.pesos_compatibilidade)
            
            comp_media /= len(self.adotantes)


            # Inserção no hank
            must_insert = False
            for i, (compat, ani_hank) in enumerate(hank):
                if comp_media > compat:
                    must_insert = True
                elif comp_media == compat:
                    if animal.idade_meses < ani_hank.idade_meses:
                        must_insert = True

                if must_insert:
                    hank.insert(i, ( comp_media, animal) )
                    hank.pop(-1)
                    break
                        
        # Adicionando os mais compatíveis ao top5
        for i, (compat, animal) in enumerate(hank):
            if compat == -1: # Garante que, caso não haja 5 animais, as compatibilidades inválidas não entram
                break

            self.top5.append(animal)

        return self.top5
            
    def exportar(self):
        """Retorna um relatório estruturado como dicionário"""
        if self.top5 is None:
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
        if len(self.adocoes):
            self.taxa = f"{((len(self.devolucoes) / len(self.adocoes)) * 100):.2f}%"
        else:
            self.taxa = f"{(0):.2f}%"

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
