
class FilaEspera:
    """Classe para modelar filas de espera no sistema

    A classe não possui herança e armazena uma lista de objetos 
    da classe EntradaFila.

    Attributes:
        animal (id - Animal): Id do animal da fila de espera.
        fila (List[EntradaFila]): Lista de entradas com interesse no animal.
    """
    pass


class EntradaFila: 
    """Classe para modelar entradas na fila de espera.

    A classe modela as entradas que serão armazenadas na 
    fina de espera de um animal. Será utilizada em conjunto com a classe FilaEspera.

    Attributes:
        adotante (id - Adotante): id do adotante considerado.
        tempo_espera (datetime): tempo de espera em horas.
        compatibilidade (float): nível de compatibilidade entre o adotante e o animal considerado.
    """
    pass
