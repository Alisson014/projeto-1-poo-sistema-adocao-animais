
class Registro:
    """Classe abstrata para modelar registros no sistema

    A classe define os atributos e métodos comuns a todos os registros
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        id (int): Id único de identificação do registro.
        animal (id - Animal): Id de identificação do animal envolvido.
        adotante (id - Adotante): Id de identificação do adotante envolvido.
    """
    pass


class Reserva(Registro):
    """ Classe para modelar reservas no sistema

    A classe herda atributos de Registro e também possui os próprios
    atributos.

    Attributes:
        data_inicial (date): Data inicial da reserva.
        data_expiracao (date): Data de expiração da reserva.
        status (ATIVA, CANCELADA, EXPIRADA): Status da reserva.
        compatibilidade (float): Compatibilidade entre os Animal e contratante envolvidos.
    """
    pass


class Adocao(Registro):
    """ Classe para modelar adoções no sistema

    A classe herda atributos de Registro e também possui os próprios
    atributos.

    Attributes:
        taxa (float): Taxa de adoção a ser cobrada.
        pago (bool): Indica se a taxa foi paga ou não.
        data (date): Data da adoção.
    """
    pass


class Devolucao(Registro):
    """ Classe para modelar devoluções no sistema

    A classe herda atributos de Registro e também possui os próprios
    atributos.

    Attributes:
        motivo (COMPORTAMENTO, PESSOAL, DOENCA, OUTRO): Tipo do motivo
        data (date): Data da devolução.
    """
    pass
