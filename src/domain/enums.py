
from enum import Enum

# Enums do sistema

# ------------------
# Animal
# ------------------

class teste:
    pass

class Sexo(Enum):
    """Sexo de um animal

    Attributes:
        MACHO.
        FEMEA.
    """
    MACHO="MACHO"
    FEMEA="FEMEA"

class Porte(Enum):
    """Porte de um animal

    Attributes:
        P: Porte pequeno.
        M: Porte médio.
        G: Porte grande.
    """
    P="P"
    M="M"
    G="G"

class StatusAnimal(Enum):
    """Status de um animal

    Attributes:
        DISPONIVEL: O animal está disponível para adoção.
        RESERVADO: O animal está em reserva.
        ADOTADO: O animal foi adotado.
        DEVOLVIDO: O animal foi devolvido.
        QUARENTENA: O animal está em quarentena.
        INADOTAVEL: O animal não pode ser adotado.
    """
    DISPONIVEL = "DISPONIVEL"
    RESERVADO = "RESERVADO"
    ADOTADO = "ADOTADO"
    DEVOLVIDO = "DEVOLVIDO"
    QUARENTENA = "QUARENTENA"
    INADOTAVEL= "INADOTAVEL"

class Energia(Enum):
    """Nível de energia de um animal

    Attributes:
        CALMO.
        HIPERATIVO.
    """
    CALMO="CALMO"
    HIPERATIVO="HIPERATIVO"

class Temperamento(Enum):
    """Temperamento de um animal

    Attributes:
        ARISCO: Pode atacar pessoas ou outros animais.
        DOCIL: Manso e sociável a pessoas e outros animais.
        MEDROSO: Esquivos, pouco sociáveis e podem acabar atacando caso se sintam ameaçados.
    """
    ARISCO="ARISCO"
    DOCIL="DOCIL"
    MEDROSO="MEDROSO"


# ------------------
# Auxiliares
# ------------------

class TipoEvento(Enum):
    """Tipo de evento registrado no histórico de um animal

    Attributes:
        VACINA.
        ADOCAO.
        DEVOLUCAO.
        QUARENTENA.
        CONSULTA.
    """
    VACINA="VACINA"
    ADOCAO="ADOCAO"
    DEVOLUCAO="DEVOLUCAO"
    QUARENTENA="QUARENTENA"
    CONSULTA="CONSULTA"


# ------------------
# Pessoa
# ------------------

class Moradia(Enum):
    """Tipo da moradia de um adotante.

    Attributes:
        APARTAMENTO_COM_VARANDA.
        APARTAMENTO_SEM_VARANDA.
        CASA_COM_QUINTAL.
        CASA_SEM_QUINTA.
    """
    APARTAMENTO_COM_VARANDA="APARTAMENTO_COM_VARANDA"
    APARTAMENTO_SEM_VARANDA="APARTAMENTO_SEM_VARANDA"
    CASA_COM_QUINTAL="CASA_COM_QUINTAL"
    CASA_SEM_QUINTA="CASA_SEM_QUINTA"

class Experiencia(Enum):
    """Nível de experiência de um adotante
    
    Attributes:
        INICIANTE: Pouca experiência.
        INTERMEDIARIO: Experiência mediana.
        AVANCADO: Muita experiência.
    """
    INICIANTE="INICIANTE"
    INTERMEDIARIO="INTERMEDIARIO"
    AVANCADO="AVANCADO"


# ------------------
# Quarentena
# ------------------

class MotivoQuarentena(Enum):
    """Motivo que levou à quarentena
    
    Attributes:
        COMPORTAMENTO.
        DOENCA.
        OUTRO.
    """
    COMPORTAMENTO="COMPORTAMENTO"
    DOENCA="DOENCA"
    OUTRO="OUTRO"

class StatusQuarentena(Enum):
    """Status de uma quarentena
    
    Attributes:
        ATIVA.
        CUMPRIDA.
    """
    ATIVA="ATIVA"
    CUMPRIDA="CUMPRIDA"


# ------------------
# Registro
# ------------------

class StatusReserva(Enum):
    """Status de uma reserva de animal
    
    Attributes:
        ATIVA.
        CANCELADA.
        EXPIRADA.
    """
    ATIVA="ATIVA"
    CANCELADA="CANCELADA"
    EXPIRADA="EXPIRADA"

class MotivoDevolucao(Enum):
    """Motivo de uma devolução
    
    Attributes:
        COMPORTAMENTO.
        PESSOAL.
        DOENCA.
        OUTRO.
    """
    COMPORTAMENTO="COMPORTAMENTO"
    PESSOAL="PESSOAL"
    DOENCA="DOENCA"
    OUTRO="OUTRO"


# ------------------
# Registros
# ------------------