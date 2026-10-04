from src.domain.mixins import AdestravelMixin, VacinavelMixin
from src.domain.enums import Sexo, Porte, StatusAnimal, Energia, Temperamento
from src.domain.models.auxiliares import Evento, Vacina
from src.domain.exceptions import (
    TipagemError,
    ValorForaDoIntervaloError,
    TransicaoDeEstadoInvalidaError,
    NaoEncontradoError,
)

from datetime import datetime


class Animal:
    """Classe abstrata para modelar animais no sistema.

    A classe define os atributos e métodos comuns a todos os animais
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        id (int): Identificador único de um animal.
        especie (string): Espécie do animal.
        nome (string): Nome do animal.
        sexo (MACHO, FEMEA): Sexo do animal
        idade_meses (int): Idade em meses do animal.
        data_entrada (datetime): Data da entrada do animal no abrigo.
        porte (P, M, G): Porte do animal.
        status (DISPONIVEL, RESERVADO, ADOTADO, DEVOLVIDO, QUARENTENA, INADOTAVEL): Estado do animal.
        energia (CALMO, HIPERATIVO): Energia do animal para atividades.
        historico (List[Evento]): Histórico de eventos do animal.
        temperamento (List[ARISCO, DÓCIL, MEDROSO]): Lista de temperamentos do animal.
        cuidado_especial (bool): Indica se o animal precisa ou não de cuidados especiais.
    """

    def __init__(
        self,
        *,
        id: int,
        especie: str,
        nome: str,
        sexo: str,
        idade_meses: int,
        porte: str,
        status: str,
        energia: str,
        cuidado_especial: bool,
        data_entrada: datetime = datetime.now(),
        historico: list[Evento] = [],
        temperamento: list[str] = [],
    ):
        self.__id: int = id  # O id de um elemento não pode ser alterado, apenas lido
        self.especie: str = especie
        self.nome: str = nome
        self.sexo: Sexo = sexo  # property setter (privado)
        self.idade_meses: int = idade_meses  # property setter (privado)
        self.data_entrada: datetime = data_entrada
        self.porte: Porte = porte  # property setter (privado)
        self.status: StatusAnimal = status  # property setter (privado)
        self.energia: Energia = energia  # property setter (privado)
        self.__historico: list[Evento] = historico
        self.temperamento: list[Temperamento] = (
            temperamento  # property setter (privado)
        )
        self.cuidado_especial: bool = cuidado_especial

    # __id: possui apenas o getter
    @property
    def id(self) -> int:
        return self.__id

    # __sexo: possui getter e setter para garantir alinhamento à tipagem
    @property
    def sexo(self) -> str:
        return self.__sexo.value

    @sexo.setter
    def sexo(self, sexo: str) -> None:
        try:
            if isinstance(Sexo(sexo), Sexo):
                self.__sexo = Sexo(sexo)
        except ValueError:
            raise TipagemError("Sexo", sexo)

    # __idade_meses: possui getter e setter para garantir validação dos dados
    @property
    def idade_meses(self) -> int:
        return self.__idade_meses

    @idade_meses.setter
    def idade_meses(self, idade_meses: int) -> None:
        if idade_meses < 0:
            raise ValorForaDoIntervaloError("idade_meses", idade_meses)

        self.__idade_meses = idade_meses

    def envelhecer(self) -> None:
        """Aumenta a idade em meses do animal com base na data de entrada"""
        data_atual: datetime = datetime.now()
        self.__idade_meses += (data_atual.year - self.data_entrada.year) * 12 + (
            data_atual.month - self.data_entrada.month
        )

        if data_atual.day < self.data_entrada.day:
            self.__idade_meses -= 1

    # __porte: possui getter e setter para garantir alinhamento à tipagem
    @property
    def porte(self) -> str:
        return self.__porte.value

    @porte.setter
    def porte(self, porte: str) -> None:
        try:
            if isinstance(Porte(porte), Porte):
                self.__porte = Porte(porte)
        except ValueError:
            raise TipagemError("Porte", porte)

    # __status: possui getter e setter para garantir alinhamento à tipagem
    @property
    def status(self) -> str:
        return self.__status.value

    @status.setter
    def status(self, status: str) -> None:
        try:
            if not self.__valida_transicao_status(StatusAnimal(status)):
                raise TransicaoDeEstadoInvalidaError(self.status, status)

            if isinstance(StatusAnimal(status), StatusAnimal):
                self.__status = StatusAnimal(status)
        except ValueError:
            raise TipagemError("StatusAnimal", status)

    # __energia: possui getter e setter para garantir alinhamento à tipagem
    @property
    def energia(self) -> str:
        return self.__energia.value

    @energia.setter
    def energia(self, energia: str) -> None:
        try:
            if isinstance(Energia(energia), Energia):
                self.__energia = Energia(energia)
        except ValueError:
            raise TipagemError("Energia", energia)

    # __temperamento: possui getter e setter para garantir alinhamento à tipagem
    @property
    def temperamento(self) -> list[Temperamento]:
        return self.__temperamento

    @temperamento.setter
    def temperamento(self, temperamento: list[str]) -> None:
        self.__temperamento = []
        try:
            for i in temperamento:
                erro = i
                isinstance(Temperamento(i), Temperamento)
                self.__temperamento.append(Temperamento(i))

        except ValueError:
            raise TipagemError("Temperamento", erro)

    # Métodos
    def adicionar_evento(self, evento: Evento) -> None:
        """Adiciona um evento ao histórico do animal"""
        if not isinstance(evento, Evento):
            raise TipagemError("Evento", evento)

        self.__historico.append(evento)

    def remover_evento(self, evento: Evento) -> None:
        """Remove evento do histórico - Hit com base nos dados do evento"""
        for i, e in enumerate(self.__historico):
            if e.__repr__ == evento.__repr__:
                self.__historico.pop(i)
                return

        raise NaoEncontradoError(type(evento).__name__)

    def get_historico(self) -> list[dict]:
        """Retorna o histórico do animal em uma lista de dicionários"""
        res = []  # variável com o conteúdo retornado
        for i in self.__historico:
            res.append(i.__dict__)

        return res

    # Método interno
    def __valida_transicao_status(self, status: StatusAnimal) -> bool:
        """Valida as transições de status"""

        # Retorna verdadeiro caso o status interno ainda não exista
        try:
            if not self.__status:
                return True
        except AttributeError:
            return True

        transicoes_validas = {
            StatusAnimal.DISPONIVEL.value: [
                StatusAnimal.RESERVADO.value,
                StatusAnimal.INADOTAVEL.value,
            ],
            StatusAnimal.RESERVADO.value: [
                StatusAnimal.ADOTADO.value,
                StatusAnimal.DISPONIVEL.value,
            ],
            StatusAnimal.ADOTADO.value: [StatusAnimal.DEVOLVIDO.value],
            StatusAnimal.DEVOLVIDO.value: [
                StatusAnimal.QUARENTENA.value,
                StatusAnimal.DISPONIVEL.value,
                StatusAnimal.INADOTAVEL.value,
            ],
            StatusAnimal.QUARENTENA.value: [
                StatusAnimal.DISPONIVEL.value,
                StatusAnimal.INADOTAVEL.value,
            ],
            StatusAnimal.INADOTAVEL.value: [],
        }

        return status in transicoes_validas[self.__status.value]


# ----------------------
# Subclasses
# ----------------------


class Cachorro(Animal, AdestravelMixin, VacinavelMixin):
    """Classe para modelar cachorros no sistema

    A classe herda os atributos de Animal, AdestravelMixin, VacinavelMixin
    e utiliza seus próprios atributos.

    Attributes:
        raca (string): Raça do cachorro.
        passeios_necessarios_dia (int): Quantidade de passeios necessária para o cachorro.
    """

    def __init__(
        self,
        *,
        id: int,
        especie: str,
        nome: str,
        sexo: str,
        idade_meses: int,
        porte: str,
        status: str,
        energia: str,
        cuidado_especial: bool,
        data_entrada: datetime = datetime.now(),
        historico: list[Evento] = [],
        temperamento: list[str] = [],
        nivel_adestramento: int = 0,
        vacinas: list[Vacina] = [],
        raca: str,
        passeios_necessarios_dia: int,
    ):
        Animal.__init__(
            self,
            id=id,
            especie=especie,
            nome=nome,
            sexo=sexo,
            idade_meses=idade_meses,
            porte=porte,
            status=status,
            energia=energia,
            cuidado_especial=cuidado_especial,
            data_entrada=data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        VacinavelMixin.__init__(self, vacinas=vacinas)
        self.raca: str = raca
        self.passeios_necessarios_dia: int = passeios_necessarios_dia

    def __str__(self) -> str:
        return f"Cachorro {self.nome}, {self.raca} {self.sexo}. É {self.energia} e está {self.status}"

    def __repr__(self) -> str:
        string = "Cachorro("
        for key, value in vars(self).items():
            string += f"{key}={value}, "
        string.rstrip()
        string += ")"

        return string


class Calopsita(Animal, AdestravelMixin):
    """Classe que modela calopsitas no sistema

    A classe herda atributos de Animal, AdestravelMixin e possui seus próprios
    atributos específicos.

    Attributes:
        canta (bool): Define se a calopsita canta ou não.
    """

    def __init__(
        self,
        *,
        id: int,
        especie: str,
        nome: str,
        sexo: str,
        idade_meses: int,
        porte: str,
        status: str,
        energia: str,
        cuidado_especial: bool,
        data_entrada: datetime = datetime.now(),
        historico: list[Evento] = [],
        temperamento: list[str] = [],
        nivel_adestramento: int = 0,
        canta: bool = False,
    ):
        Animal.__init__(
            self,
            id=id,
            especie=especie,
            nome=nome,
            sexo=sexo,
            idade_meses=idade_meses,
            porte=porte,
            status=status,
            energia=energia,
            cuidado_especial=cuidado_especial,
            data_entrada=data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        self.__canta: bool = canta  # acessado via getter property

    @property
    def canta(self):
        return self.__canta

    def ensinar_a_cantar(self):
        self.__canta = True

    def __str__(self) -> str:
        return f"Calopsita {self.nome} {self.sexo}. É {self.energia} e está {self.status}"

    def __repr__(self) -> str:
        string = "Calopsita("
        for key, value in vars(self).items():
            string += f"{key}={value}, "
        string.rstrip()
        string += ")"
        return string

class Coelho(Animal, AdestravelMixin, VacinavelMixin):
    """Classe para modelar coelhos no sistema

    A classe herda atributos da classe Animal, AdestravelMixin, VacinavelMixin e possui seus
    próprios atributos específicos.

    Attributes:
        raca (string): Raça do coelho.
        tamanho_gaiola_cm3 (float): Tamanho de gaiola necessário em centimetros cúbicos.
    """

    def __init__(
        self,
        *,
        id: int,
        especie: str,
        nome: str,
        sexo: str,
        idade_meses: int,
        porte: str,
        status: str,
        energia: str,
        cuidado_especial: bool,
        data_entrada: datetime = datetime.now(),
        historico: list[Evento] = [],
        temperamento: list[str] = [],
        nivel_adestramento: int = 0,
        vacinas: list[Vacina] = [],
        raca: str,
        tamanho_gaiola_m3: float,
    ):
        Animal.__init__(
            self,
            id=id,
            especie=especie,
            nome=nome,
            sexo=sexo,
            idade_meses=idade_meses,
            porte=porte,
            status=status,
            energia=energia,
            cuidado_especial=cuidado_especial,
            data_entrada=data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        VacinavelMixin.__init__(self, vacinas=vacinas)
        self.raca: str = raca
        self.tamanho_gaiola_m3: int = tamanho_gaiola_m3  # property setter (privado)

    @property
    def tamanho_gaiola_m3(self):
        return self.__tamanho_gaiola_m3

    @tamanho_gaiola_m3.setter
    def tamanho_gaiola_m3(self, tamanho_gaiola_m3):
        if tamanho_gaiola_m3 < 0.35:
            raise ValorForaDoIntervaloError("tamanho_gaiola_m3", tamanho_gaiola_m3)
        self.__tamanho_gaiola_m3 = tamanho_gaiola_m3

    def __str__(self) -> str:
        return f"Coelho {self.nome}, {self.raca} {self.sexo}. É {self.energia} e está {self.status}"

    def __repr__(self) -> str:
        string = "Coelho("
        for key, value in vars(self).items():
            string += f"{key}={value}, "
        string.rstrip()
        string += ")"
        return string



class Gato(Animal, AdestravelMixin, VacinavelMixin):
    """Classe para modelar gatos no sistema

    A classe herda atributos da classe Animal, AdestravelMixin, VacinavelMixin e possui seus próprios
    atributos específicos.

    Attributes:
        raca (string): Raça do gato.
        independencia (bool): Indica se o gato apresenta ou não independência.
    """

    def __init__(
        self,
        *,
        id: int,
        especie: str,
        nome: str,
        sexo: str,
        idade_meses: int,
        porte: str,
        status: str,
        energia: str,
        cuidado_especial: bool,
        data_entrada: datetime = datetime.now(),
        historico: list[Evento] = [],
        temperamento: list[str] = [],
        nivel_adestramento: int = 0,
        vacinas: list[Vacina] = [],
        raca: str,
        independencia: bool,
    ):
        Animal.__init__(
            self,
            id=id,
            especie=especie,
            nome=nome,
            sexo=sexo,
            idade_meses=idade_meses,
            porte=porte,
            status=status,
            energia=energia,
            cuidado_especial=cuidado_especial,
            data_entrada=data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        VacinavelMixin.__init__(self, vacinas=vacinas)
        self.raca: str = raca
        self.independencia: bool = independencia

    def __str__(self) -> str:
            return f"Gato {self.nome}, {self.raca} {self.sexo}. É {self.energia} e está {self.status}"
    
    def __repr__(self) -> str:
        string = "Gato("
        for key, value in vars(self).items():
            string += f"{key}={value}, "
        string.rstrip()
        string += ")"
        return string
