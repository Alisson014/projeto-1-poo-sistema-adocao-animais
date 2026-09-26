
class Relatorio:
    """Classe abstrata para modelar relatorios no sistema.

    A classe define os atributos e métodos comuns a todos os relatórios 
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        id (int): Identificador único do relatório.
        data (date): Data de criação do relatório.
        nome (string): Nome do relatório.
    """
    pass


class Top5MaisAdotaveis(Relatorio):
    """Classe para modelar relatórios de animais mais adotáveis

    A classe herda atributos de Relatório e também possui os próprios 
    atributos específicos.

    Attributes:
        animais (List[Animal]): Lista de animais considerada no momento da criação.
        Adotantes (List[Adotante]): Lista de adotantes considerada no momento da criação.
        top5 (List[Animal]): Lista dos 5 animais mais adotáveis.
    """
    pass


class TaxaAdocaoEspecies(Relatorio):
    """Classe para modelar os relatórios com as taxas de adoção por Animais.

    A classe herda atributos de Relatório e também possui os próprios 
    atributos específicos.

    Attributes:
        adocoes (List[Adocao]): Lista das adoções consideradas;
        taxas (dict): Dicionário que armazenas os pares de chave e valor {"Animal": "adotados/Total"}
    """
    pass


class TaxaAdocaoPorte(Relatorio):
    """Classe para modelar os relatórios com as taxas de adoção por portes.

    A classe herda atributos de Relatório e também possui os próprios 
    atributos específicos.

    Attributes:
        adocoes (List[Adocao]): Lista das adoções consideradas;
        taxas (dict): Dicionário que armazenas os pares de chave e valor {"Porte": "adotados/Total"}
    """
    pass


class TaxaTempoMedioEntradaAdocao(Relatorio):
    """Classe para modelar os relatórios com o tempo médio entre entrada e adoção.

    A classe herda atributos de Relatório e também possui os próprios 
    atributos específicos.

    Attributes:
        animais (List[Animal]): Animais considerados no relatório.
        adocoes (List[Adocao]): Adoções consideradas no relatório.
        tempo_medio_dias (int): Tempo médio em dias.
    """
    pass


class TaxaDevolucoes(Relatorio):
    """Classe para modelar os relatórios com a taxa entre adoções e devoluções;

    A classe herda atributos de Relatório e também possui os próprios 
    atributos específicos.

    Attributes:
        data_inicial (date): Data inicial considerada para a análise.
        data_final (date): Data final considerada para a análise.
        adocoes (List[Adocao]): Lista de adoções considerada.
        devolucoes (List[Devolucao]): Lista de devoluções considerada.
    """
    pass
