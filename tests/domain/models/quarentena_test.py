from src.domain.models import Quarentena
from src.domain.exceptions import *

from datetime import datetime

import pytest


# Testes Quarentena


def test_cria_quarentena():
    quarentena = Quarentena(
        animal=1, data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
    )
    assert quarentena


def test_cria_quarentena_motivo_error():
    with pytest.raises(TipagemError):
        quarentena = Quarentena(
            animal=1, data_inicial=datetime.now(), motivo="INVALIDO", status="CUMPRIDA"
        )


def test_cria_quarentena_status_error():
    with pytest.raises(TipagemError):
        quarentena = Quarentena(
            animal=1, data_inicial=datetime.now(), motivo="OUTRO", status="INVALIDO"
        )
