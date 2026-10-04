# Exceções customizadas


class ValorForaDoIntervaloError(Exception):
    """Para tratamentos de valores númericos fora do intervalo permitido"""

    def __init__(self, atributo_name: str, atributo_value: object):
        super().__init__(
            f"Valor fora do intervalor permitido: {atributo_name}=({atributo_value})"
        )
        self.atributo_name: str = atributo_name
        self.atributo_value: object = atributo_value


class TipagemError(Exception):
    """Para tratar erros de tipagem com enums"""

    def __init__(self, type_name: str, value: object):
        super().__init__(f"Tipagem inválida: {type_name} não tem {value}")
        self.type_name: str = type_name
        self.value: object = value


class TransicaoDeEstadoInvalidaError(Exception):
    """Para tratar transições de estado inválidas"""

    def __init__(self, atual: str, nova: str):
        super().__init__(f"A transição de {atual} para {nova} é inválida")
        self.atual: str = atual
        self.nova: str = nova


class NaoEncontradoError(Exception):
    """Para tratar error de objeto não encontrado"""

    def __init__(self, obj_name: str):
        super().__init__(f"{obj_name} não encontrado")
        self.obj_name = obj_name


class EmailInvalidoError(Exception):
    """Para tratar emails inválidos"""

    def __init__(self, email: str):
        super().__init__(f"{email} inválido")
        self.email = email


class RelatorioNaoGeradoError(Exception):
    def __init__(self):
        super().__init__("É preciso gerar o conteúdo do relatório")


# Define explicitamente o que é exportado
__all__ = [
    "ValorForaDoIntervaloError",
    "TipagemError",
    "TransicaoDeEstadoInvalidaError",
    "NaoEncontradoError",
    "EmailInvalidoError",
    "RelatorioNaoGeradoError",
]
