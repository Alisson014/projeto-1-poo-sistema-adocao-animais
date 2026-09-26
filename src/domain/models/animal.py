
from src.domain.mixins import AdestravelMixin, VacinavelMixin

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
        data_entrada (Date): Data da entrada do animal no abrigo.
        porte (P, M, G): Porte do animal.
        status (DISPONIVEL, RESERVADO, ADOTADO, DEVOLVIDO, QUARENTENA, INADOTAVEL): Estado do animal.
        energia (CALMO, HIPERATIVO): Energia do animal para atividades.
        historico (List[Evento]): Histórico de eventos do animal.
        temperamento (List[ARISCO, DÓCIL, MEDROSO]): Lista de temperamentos do animal.
        cuidado_especial (bool): Indica se o animal precisa ou não de cuidados especiais.
    """
    pass



class Cachorro(Animal, AdestravelMixin, VacinavelMixin):
    """Classe para modelar cachorros no sistema
    
    A classe herda os atributos de Animal, AdestravelMixin, VacinavelMixin 
    e utiliza seus próprios atributos.

    Attributes:
        raca (string): Raça do cachorro.
        passeios_necessarios_dia (int): Quantidade de passeios necessária para o cachorro.
    """
    pass


class Calopsita(Animal, AdestravelMixin):
    """Classe que modela calopsitas no sistema

    A classe herda atributos de Animal, AdestravelMixin e possui seus próprios 
    atributos específicos.

    Attributes:
        canta (bool): Define se a calopsita canta ou não.
    """
    pass


class Coelho(Animal, AdestravelMixin, VacinavelMixin):
    """Classe para modelar coelhos no sistema

    A classe herda atributos da classe Animal, AdestravelMixin, VacinavelMixin e possui seus 
    próprios atributos específicos.

    Attributes:
        raca (string): Raça do coelho.
        tamanho_gaiola_cm2 (float): Tamanho de gaiola necessário em centimetros quadrados.
    """
    pass


class Gato(Animal, AdestravelMixin, VacinavelMixin):
    """Classe para modelar gatos no sistema

    A classe herda atributos da classe Animal, AdestravelMixin, VacinavelMixin e possui seus próprios
    atributos específicos.

    Attributes:
        raca (string): Raça do gato.
        independencia (bool): Indica se o gato apresenta ou não independência.
    """
    pass