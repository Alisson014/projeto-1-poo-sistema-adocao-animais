
class Pessoa:
    """Clase abstrata para modelar pessoas no sistema
    
    A classe define os atributos e métodos comuns a todas as pessoas
    cadastradas no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        nome (string): Nome da pessoa.
        email (string): Email para identificar uma pessoa.
        idade (int): Idade da pessoa em anos.
    """
    pass


class Adotante(Pessoa):
    """Classe para modelar adotantes no sistema

    A classe herda atributos de Pessoa e possui 
    os próprios atributos específicos.

    Attributes:
        moradia (APARTAMENTO_COM_VARANDA, APARTAMENTO_SEM_VARANDA, CASA_COM_QUINTAL, CASA_SEM_QUINTAL): Tipo de moradia.
        experiencia (INICIANTE, INTERMEDIÁRIO, AVANÇADO): Experiência com animais.
        tempo_livre_min (int): Tempo livre médio em minutos.
        possui_criancas (bool): Indica se pessui crianças ou não.
        outros_animais (bool): Indica se possui outros animais ou não.
        area_util (float): Area útil da residência em metros quadrados.
    """
    pass
