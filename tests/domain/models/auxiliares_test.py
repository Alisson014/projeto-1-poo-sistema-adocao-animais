from src.domain.models import Evento, Vacina
from src.domain.exceptions import *

from datetime import datetime

import pytest


# Testes Evento
def test_cria_evento():
    evento = Evento(tipo="VACINA", descricao="descricao", data=datetime.now())
    assert evento


def test_cria_evento_erro_tipo():
    with pytest.raises(TipagemError):
        evento = Evento(tipo="INVALIDO", descricao="descricao", data=datetime.now())


# Testes Vacina
def test_cria_vacina():
    vacina = Vacina(nome="nome", data=datetime.now())
    assert vacina
