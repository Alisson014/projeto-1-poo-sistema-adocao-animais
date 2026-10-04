from src.domain.enums import Porte

from abc import ABC, abstractmethod
from datetime import datetime


class Politica(ABC):
    """Classe abstrata para modelar políticas configuráveis no sistema.

    A classe define os atributos e métodos comuns a todos as políticas
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        nome (string): Nome da política.
        data_modificacao (datetime): Data da última modificação realizada.
    """

    def __init__(self, *, nome: str, data_modificacao: datetime):
        self.nome: str = nome
        self.data_modificacao: datetime = data_modificacao

    @abstractmethod
    def validar(self) -> bool:
        pass


class IdadeMinima(Politica):
    """Classe para modelar a política de idade mínima.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        idade_minima (int): Idade mínima para adotar um animal
    """

    def __init__(self, *, nome: str, data_modificacao: datetime, idade_minima: int):
        super().__init__(nome=nome, data_modificacao=data_modificacao)
        self.idade_minima: int = idade_minima

    def validar(self, idade) -> bool:  # type: ignore[override]
        return idade >= self.idade_minima

    def __str__(self):
        return f"Política de Idade mínima, idade_minima = {self.idade_minima}"

    def __repr__(self):
        return f"IdadeMinima(idade_minina={self.idade_minima})"


class PorteXArea(Politica):
    """Classe para modelar a política de áreas mínimas para cada porte.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        porte_p_min (float): Área mínima para o porte P em metros quadrados.
        porte_m_min (float): Área mínima para o porte M em metros quadrados.
        porte_g_min (float): Área mínima para o porte G em metros quadrados.
    """

    def __init__(
        self,
        *,
        nome: str,
        data_modificacao: datetime,
        porte_p_min: float,
        porte_m_min: float,
        porte_g_min: float,
    ):
        super().__init__(nome=nome, data_modificacao=data_modificacao)
        self.porte_p_min: float = porte_p_min
        self.porte_m_min: float = porte_m_min
        self.porte_g_min: float = porte_g_min

    def validar(self, porte: Porte, area: float) -> bool:  # type: ignore[override]
        portes_area = {
            Porte.P.value: self.porte_p_min,
            Porte.M.value: self.porte_m_min,
            Porte.G.value: self.porte_g_min,
        }

        return area >= portes_area[porte.value]

    def __str__(self):
        return f"Política de Area por Porte, Porte p({self.porte_p_min}) - Porte m({self.porte_m_min}) - Porte g({self.porte_g_min})"
    
    def __repr__(self):
        return f"PorteXArea(porte_p_min={self.porte_p_min}, porte_m_min={self.porte_m_min}, porte_g_min={self.porte_g_min})"


class DuracaoReserva(Politica):
    """Classe para modelar a política de duração de reservas.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        duracao_dias (int): Duração de reservas em dias.
    """

    def __init__(self, *, nome: str, data_modificacao: datetime, duracao_dias: int):
        super().__init__(nome=nome, data_modificacao=data_modificacao)
        self.duracao_dias: int = duracao_dias

    def __str__(self):
        return f"Política de Duaração da reserva, duração = {self.duracao_dias} dias"

    def __repr__(self):
        return f"DuracaoReserva(duracao_dias={self.duracao_dias})"


class PesosCompatibilidade(Politica):
    """Classe para modelar a política de pesos dos fatores de compatibilidade.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        peso_porte_moradia (float);
        peso_experiencia_temperamento (float);
        peso_tempo_livre_energia (float);
        peso_criancas_temperamento (float);
    """

    def __init__(
        self,
        *,
        nome: str,
        data_modificacao: datetime,
        peso_porte_moradia: float,
        peso_experiencia_temperamento: float,
        peso_tempo_livre_energia: float,
        peso_criancas_temperamento: float,
    ):
        super().__init__(nome=nome, data_modificacao=data_modificacao)
        self.peso_porte_moradia: float = peso_porte_moradia
        self.peso_experiencia_temperamento: float = peso_experiencia_temperamento
        self.peso_tempo_livre_energia: float = peso_tempo_livre_energia
        self.peso_criancas_temperamento: float = peso_criancas_temperamento

    def __str__(self):
        return f"Política de Pesos para compatibilidade, porte X moradia({self.peso_porte_moradia}), experiência X temperamento({self.peso_experiencia_temperamento}), tempo livre X energia({self.peso_tempo_livre_energia}). crianças X temperamento=({self.peso_criancas_temperamento})"
    
    def __repr__(self):
        return f"PesosCompatibilidade(peso_porte_moradia={self.peso_porte_moradia}), peso_experiencia_temperamento=({self.peso_experiencia_temperamento}), peso_tempo_livre_energia=({self.peso_tempo_livre_energia}). peso_criancas_temperamento=({self.peso_criancas_temperamento})"
