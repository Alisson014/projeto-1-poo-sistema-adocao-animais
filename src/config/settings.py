
class Politica:
    """Classe abstrata para modelar políticas configuráveis no sistema.

    A classe define os atributos e métodos comuns a todos as políticas 
    cadastrados no sistema, com o intuito de reaproveitar código e dinamizar o desenvolvimento.

    Attributes:
        nome (string): Nome da política.
        data_modificacao (date): Data da última modificação realizada.
    """
    pass


class IdadeMinima():
    """Classe para modelar a política de idade mínima.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        idade_minina (int): Idade mínima para adotar um animal
    """
    pass


class PorteXArea():
    """Classe para modelar a política de áreas mínimas para cada porte.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        porte_p_min (float): Área mínima para o porte P em metros quadrados.
        porte_m_min (float): Área mínima para o porte M em metros quadrados.
        porte_g_min (float): Área mínima para o porte G em metros quadrados.
    """
    pass


class DuracaoReserva():
    """Classe para modelar a política de duração de reservas.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        duracao_dias (int): Duração de reservas em dias.
    """
    pass


class PesosCompatibilidade():
    """Classe para modelar a política de pesos dos fatores de compatibilidade.

    A classe herda os atributos de Politica e utiliza seus próprios atributos.

    Attributes:
        peso_porte_moradia (float);
        peso_experiencia_temperamento (float);
        peso_tempo_livre_energia (float);
        peso_criancas_temperamento (float);
    """
    pass
