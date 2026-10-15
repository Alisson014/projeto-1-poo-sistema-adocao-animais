from src.domain.mixins import AdestravelMixin, VacinavelMixin
from src.domain.enums import Sexo, Porte, StatusAnimal, Energia, Temperamento
from src.domain.models.auxiliares import Evento, Vacina
from src.domain.exceptions import (
    TipagemError,
    ValorForaDoIntervaloError,
    TransicaoDeEstadoInvalidaError,
    NaoEncontradoError,
)

from datetime import datetime, date
from abc import abstractmethod


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

    # ====================
    # Properties
    # ====================

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
            # Se não for válido, essa verificação dispara um erro
            # Evitando que o estado seja alterado
            if isinstance(Sexo(sexo), Sexo):
                # Valida se a string é um Sexo válido
                self.__sexo = Sexo(sexo)
        except ValueError:
            raise TipagemError("Sexo", sexo)

    # __idade_meses: possui getter e setter para garantir validação dos dados
    @property
    def idade_meses(self) -> int:
        return self.__idade_meses

    @idade_meses.setter
    def idade_meses(self, idade_meses: int) -> None:
        # Checa se a idade não é menor que zero
        # Uma exceção customizada é disparada caso seja
        if idade_meses < 0:
            raise ValorForaDoIntervaloError("idade_meses", idade_meses)

        self.__idade_meses = idade_meses

    # __porte: possui getter e setter para garantir alinhamento à tipagem
    @property
    def porte(self) -> str:
        return self.__porte.value

    @porte.setter
    def porte(self, porte: str) -> None:
        try:
            # Se não for válido, essa verificação dispara um erro
            # Evitando que o estado seja alterado
            if isinstance(Porte(porte), Porte):
                # Valida se a string é um Porte válido
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
            # Valida se a transição de status é permitida
            # Caso não seja, um erro é disparado e tratado como TransicaoDeEstadoInvalidaError
            # A conversão de StatusAnimal na função trata automáticamente a validade do parâmetro
            if not self.__valida_transicao_status(StatusAnimal(status)):
                raise TransicaoDeEstadoInvalidaError(self.status, status)

            # Atribui um StatusAnimal válido ao atributo
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
            # Se não for válido, essa verificação dispara um erro
            # Evitando que o estado seja alterado
            if isinstance(Energia(energia), Energia):
                # Valida se a string é uma Energia válida
                self.__energia = Energia(energia)
        except ValueError:
            raise TipagemError("Energia", energia)

    # __temperamento: possui getter e setter para garantir alinhamento à tipagem
    @property
    def temperamento(self) -> list[Temperamento]:
        return self.__temperamento

    @temperamento.setter
    def temperamento(self, temperamento: list[str]) -> None:
        try:
            # lista temporária para validação
            temperamentos_validos = []
            for i in temperamento:
                # Variável para capturar o temperamento na lista que não corresponte a um Temperamento válido
                temperamento_invalido = i

                # Temperamento(i) válida automaticamente se i é válido ou não
                temperamentos_validos.append(Temperamento(i))

            # O atributos só é alterado se todos os temperamentos forem válidos
            self.__temperamento = temperamentos_validos
        except ValueError:
            raise TipagemError("Temperamento", temperamento_invalido)

    # ====================
    # Métodos
    # ====================

    # Método de classe abstrato para ser reescrito pelas classes filhas
    @classmethod
    def from_dict(cls, animal: dict):
        pass

    # Método abstrato para ser reescrito pelas classes filhas:
    @abstractmethod
    def to_dict(self):
        pass

    def envelhecer(self) -> None:
        """Aumenta a idade em meses do animal com base na data de entrada"""
        data_atual: datetime = datetime.now()

        # Calcular o incremento em meses comparando a data atual com a data de entrada
        incremento = (data_atual.year - self.data_entrada.year) * 12 + (
            data_atual.month - self.data_entrada.month
        )

        # Desconta um mês a depender do dia atual
        if data_atual.day < self.data_entrada.day:
            incremento -= 1

        # A idade é incrementada apenas se a idade do animal não estiver atualizada
        # Evita que um animal envelheça se a idade registrada já bater com a idade real
        self.__idade_meses += (
            incremento if self.__idade_meses + incremento != self.__idade_meses else 0
        )

    def adicionar_evento(self, evento: Evento) -> None:
        """Adiciona um evento ao histórico do animal"""
        try:
            # Caso o evento seja inválido um erro é disparado
            isinstance(evento, Evento)
        except:
            raise TipagemError("Evento", evento)

        # O evento só é adicionado se for válido
        self.__historico.append(evento)

    def remover_evento(self, evento: Evento) -> None:
        """Remove evento do histórico - Hit com base nos dados do evento"""
        try:
            # Caso o evento seja inválido um erro é disparado
            isinstance(evento, Evento)
        except:
            raise TipagemError("Evento", evento)

        for i, e in enumerate(self.__historico):
            # Verfica se os objetos são iguis com base na string do repr
            # Anotação para depois, definir o __eq__ para a classse
            if repr(e) == repr(evento):
                self.__historico.pop(i)
                return

        raise NaoEncontradoError(type(evento).__name__)

    def get_temperamento(self) -> list[str]:
        res = []
        for i in self.temperamento:
            res.append(i.value)

        return res

    def get_historico(self) -> list[dict]:
        """Retorna o histórico do animal em uma lista de dicionários"""
        res = []  # variável com o conteúdo retornado
        for i in self.__historico:
            # Converte cada evento do histórico para um dicionário
            res.append(i.to_dict())

        return res

    # Método interno
    def __valida_transicao_status(self, status: StatusAnimal) -> bool:
        """Valida as transições de status"""

        try:
            # Retorna verdadeiro caso o status interno ainda não exista
            if not self.__status:
                return True
        except AttributeError:
            return True

        # Dicionário que associa cada status a uma lista com as transições
        # permitidas para o respectivo status
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

        # Retorna um boolean que indica a validade da operação
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
            data_entrada=datetime.fromisoformat(data_entrada)
            if isinstance(data_entrada, str)
            else data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        VacinavelMixin.__init__(self, vacinas=vacinas)
        self.raca: str = raca
        self.passeios_necessarios_dia: int = passeios_necessarios_dia

    @classmethod
    def from_dict(cls, animal: dict):
        # Converte os dicionários de vacinas em instâncias
        key_vacinas = animal.pop("vacinas")
        vacinas: list[Vacina] = []
        for i in key_vacinas:
            vacinas.append(Vacina.from_dict(i))

        # Converte os dicionários de eventos em instâncias
        key_historico = animal.pop("historico")
        historico: list[Evento] = []
        for i in key_historico:
            historico.append(Evento.from_dict(i))

        return cls(**animal, vacinas=vacinas, historico=historico)

    def to_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "status": self.status,
            "energia": self.energia,
            "cuidado_especial": self.cuidado_especial,
            "data_entrada": self.data_entrada.__str__(),
            "historico": self.get_historico(),
            "temperamento": self.get_temperamento(),
            "nivel_adestramento": self.nivel_adestramento,
            "vacinas": [vacina.to_dict() for vacina in self.vacinas],
            "raca": self.raca,
            "passeios_necessarios_dia": self.passeios_necessarios_dia,
        }

    def __str__(self) -> str:
        return f"Cachorro {self.nome}, {self.raca} {self.sexo}. É {self.energia} e está {self.status}"

    def __repr__(self) -> str:
        string = "Cachorro("

        # Itera sobre os atributos de self e adiciona todos programáticamente
        for key, value in self.to_dict().items():
            string += f"{key}={value}, "

        # Elimina o espaço do último atributo
        string.rstrip()
        string += ")"

        return string

    def __eq__(self, outro_animal: object) -> bool:
        if not isinstance(outro_animal, Cachorro):
            return NotImplemented
        return self.id == outro_animal.id

    def __lt__(self, outro_animal: object) -> bool:
        """Utilizado para verificar se um animal é mais novo que outro"""
        if not isinstance(outro_animal, Cachorro):
            return NotImplemented
        return self.idade_meses < outro_animal.idade_meses


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
            data_entrada=datetime.fromisoformat(data_entrada)
            if isinstance(data_entrada, str)
            else data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        self.__canta: bool = canta  # acessado via getter property

    # canta possui apenas o getter para garatir que só possa ser alterado via ensinar_a_canta()
    @property
    def canta(self):
        return self.__canta

    def ensinar_a_cantar(self):
        self.__canta = True

    @classmethod
    def from_dict(cls, animal: dict):
        # Converte os dicionários de eventos em instâncias
        key_historico = animal.pop("historico")
        historico: list[Evento] = []
        for i in key_historico:
            historico.append(Evento.from_dict(i))

        return cls(**animal, historico=historico)

    def to_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "status": self.status,
            "energia": self.energia,
            "cuidado_especial": self.cuidado_especial,
            "data_entrada": self.data_entrada.__str__(),
            "historico": self.get_historico(),
            "temperamento": self.get_temperamento(),
            "nivel_adestramento": self.nivel_adestramento,
            "canta": self.canta,
        }

    def __str__(self) -> str:
        return (
            f"Calopsita {self.nome} {self.sexo}. É {self.energia} e está {self.status}"
        )

    def __repr__(self) -> str:
        string = "Calopsita("
        # Itera sobre os atributos de self e adiciona todos programáticamente
        for key, value in self.to_dict().items():
            string += f"{key}={value}, "
        # Elimina o espaço do último atributo
        string.rstrip()
        string += ")"
        return string

    def __eq__(self, outro_animal: object) -> bool:
        if not isinstance(outro_animal, Calopsita):
            return NotImplemented
        return self.id == outro_animal.id

    def __lt__(self, outro_animal: object) -> bool:
        """Utilizado para verificar se um animal é mais novo que outro"""
        if not isinstance(outro_animal, Calopsita):
            return NotImplemented
        return self.idade_meses < outro_animal.idade_meses


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
            data_entrada=datetime.fromisoformat(data_entrada)
            if isinstance(data_entrada, str)
            else data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        VacinavelMixin.__init__(self, vacinas=vacinas)
        self.raca: str = raca
        self.tamanho_gaiola_m3: int = tamanho_gaiola_m3  # property setter (privado)

    # tamanho_gaiola_m3 possui getter e setter para garantir validação
    @property
    def tamanho_gaiola_m3(self):
        return self.__tamanho_gaiola_m3

    @tamanho_gaiola_m3.setter
    def tamanho_gaiola_m3(self, tamanho_gaiola_m3):
        # Verifica se o tamanho está de acordo com o mínimo permitido
        if tamanho_gaiola_m3 < 0.35:
            raise ValorForaDoIntervaloError("tamanho_gaiola_m3", tamanho_gaiola_m3)
        self.__tamanho_gaiola_m3 = tamanho_gaiola_m3

    @classmethod
    def from_dict(cls, animal: dict):
        # Converte os dicionários de vacinas em instâncias
        key_vacinas = animal.pop("vacinas")
        vacinas: list[Vacina] = []
        for i in key_vacinas:
            vacinas.append(Vacina.from_dict(i))

        # Converte os dicionários de eventos em instâncias
        key_historico = animal.pop("historico")
        historico: list[Evento] = []
        for i in key_historico:
            historico.append(Evento.from_dict(i))

        return cls(**animal, vacinas=vacinas, historico=historico)

    def to_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "status": self.status,
            "energia": self.energia,
            "cuidado_especial": self.cuidado_especial,
            "data_entrada": self.data_entrada.__str__(),
            "historico": self.get_historico(),
            "temperamento": self.get_temperamento(),
            "nivel_adestramento": self.nivel_adestramento,
            "vacinas": [vacina.to_dict() for vacina in self.vacinas],
            "raca": self.raca,
            "tamanho_gaiola_m3": self.tamanho_gaiola_m3,
        }

    def __str__(self) -> str:
        return f"Coelho {self.nome}, {self.raca} {self.sexo}. É {self.energia} e está {self.status}"

    def __repr__(self) -> str:
        string = "Coelho("
        # Itera sobre os atributos de self e adiciona todos programáticamente
        for key, value in self.to_dict().items():
            string += f"{key}={value}, "
        # Elimina o espaço do último atributo
        string.rstrip()
        string += ")"
        return string

    def __eq__(self, outro_animal: object) -> bool:
        if not isinstance(outro_animal, Coelho):
            return NotImplemented
        return self.id == outro_animal.id

    def __lt__(self, outro_animal: object) -> bool:
        """Utilizado para verificar se um animal é mais novo que outro"""
        if not isinstance(outro_animal, Coelho):
            return NotImplemented
        return self.idade_meses < outro_animal.idade_meses


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
            data_entrada=datetime.fromisoformat(data_entrada)
            if isinstance(data_entrada, str)
            else data_entrada,
            historico=historico,
            temperamento=temperamento,
        )
        AdestravelMixin.__init__(self, nivel_adestramento=nivel_adestramento)
        VacinavelMixin.__init__(self, vacinas=vacinas)
        self.raca: str = raca
        self.independencia: bool = independencia

    @classmethod
    def from_dict(cls, animal: dict):
        # Converte os dicionários de vacinas em instâncias
        key_vacinas = animal.pop("vacinas")
        vacinas: list[Vacina] = []
        for i in key_vacinas:
            vacinas.append(Vacina.from_dict(i))

        # Converte os dicionários de eventos em instâncias
        key_historico = animal.pop("historico")
        historico: list[Evento] = []
        for i in key_historico:
            historico.append(Evento.from_dict(i))

        return cls(**animal, vacinas=vacinas, historico=historico)

    def to_dict(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "status": self.status,
            "energia": self.energia,
            "cuidado_especial": self.cuidado_especial,
            "data_entrada": self.data_entrada.__str__(),
            "historico": self.get_historico(),
            "temperamento": self.get_temperamento(),
            "nivel_adestramento": self.nivel_adestramento,
            "vacinas": [vacina.to_dict() for vacina in self.vacinas],
            "raca": self.raca,
            "independencia": self.independencia,
        }

    def __str__(self) -> str:
        return f"Gato {self.nome}, {self.raca} {self.sexo}. É {self.energia} e está {self.status}"

    def __repr__(self) -> str:
        string = "Gato("
        # Itera sobre os atributos de self e adiciona todos programáticamente
        for key, value in vars(self).items():
            string += f"{key}={value}, "
        # Elimina o espaço do último atributo
        string.rstrip()
        string += ")"
        return string

    def __eq__(self, outro_animal: object) -> bool:
        if not isinstance(outro_animal, Gato):
            return NotImplemented
        return self.id == outro_animal.id

    def __lt__(self, outro_animal: object) -> bool:
        """Utilizado para verificar se um animal é mais novo que outro"""
        if not isinstance(outro_animal, Gato):
            return NotImplemented
        return self.idade_meses < outro_animal.idade_meses
