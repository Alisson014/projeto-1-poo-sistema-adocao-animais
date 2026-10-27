from src.config import PorteXArea, PesosCompatibilidade, DuracaoReserva, IdadeMinima, Politica
from src.repositories import PoliticaRepository

from datetime import datetime
import pytest

path = "tests/data/settings.json"

settings_repository = PoliticaRepository(path)

porte_x_area = PorteXArea(nome="porte x area", data_modificacao=datetime.now(), porte_p_min=20, porte_m_min=40, porte_g_min=60)
pesos_compatibilidade = PesosCompatibilidade(nome="pesos compatibilidade", data_modificacao=datetime.now(), peso_porte_moradia=0.2, peso_experiencia_temperamento=0.3, peso_tempo_livre_energia=0.2, peso_criancas_temperamento=0.3)
duracao_reserva = DuracaoReserva(nome="duração reserva", data_modificacao=datetime.now(), duracao_dias=14)
idade_minima = IdadeMinima(nome="idade mínima", data_modificacao=datetime.now(), idade_minima=18)

# A intenção deste teste é limpar automaticamente settings.json para evitar erros na criação de políticas já existentes
def test_delete_all_settings():
    settings_repository.delete_all(validator=True)

def test_create_PorteXArea():
    assert settings_repository.create(porte_x_area)

def test_create_PesosCompatibilidade():
    assert settings_repository.create(pesos_compatibilidade)

def test_create_DuracaoReserva():
    assert settings_repository.create(duracao_reserva)

def test_create_IdadeMinima():
    assert settings_repository.create(idade_minima)

def test_get_all_settings():
    politicas = settings_repository.get_all()

    for i in politicas:
        assert isinstance(i, Politica)

def test_get_by_name_PorteXArea():
    politica = settings_repository.get_by_name("PorteXArea")
    assert isinstance(politica, PorteXArea)
    assert repr(politica) == repr(porte_x_area)

def test_get_by_name_PesosCompatibilidade():
    politica = settings_repository.get_by_name("PesosCompatibilidade")
    assert isinstance(politica, PesosCompatibilidade)
    assert repr(politica) == repr(pesos_compatibilidade)

def test_get_by_name_DuracaoReserva():
    politica = settings_repository.get_by_name("DuracaoReserva")
    assert isinstance(politica, DuracaoReserva)
    assert repr(politica) == repr(duracao_reserva)

def test_get_by_name_IdadeMinima():
    politica = settings_repository.get_by_name("IdadeMinima")
    assert isinstance(politica, IdadeMinima)
    assert repr(politica) == repr(idade_minima)

def test_update_PorteXArea():
    politica = settings_repository.get_by_name("PorteXArea")

    politica.porte_g_min = 100
    settings_repository.update(politica)

    new_politica = settings_repository.get_by_name("PorteXArea")

    assert repr(politica) == repr(new_politica)

def test_update_PesosCompatibilidade():
    politica = settings_repository.get_by_name("PesosCompatibilidade")

    politica.nome = "Pesos compatibilidade"
    settings_repository.update(politica)

    new_politica = settings_repository.get_by_name("PesosCompatibilidade")

    assert repr(politica) == repr(new_politica)

def test_update_DuracaoReserva():
    politica = settings_repository.get_by_name("DuracaoReserva")

    politica.duracao_dias = 15
    settings_repository.update(politica)

    new_politica = settings_repository.get_by_name("DuracaoReserva")

    assert repr(politica) == repr(new_politica)

def test_update_IdadeMinima():
    politica = settings_repository.get_by_name("IdadeMinima")

    politica.nome = "Idade mínima"
    settings_repository.update(politica)

    new_politica = settings_repository.get_by_name("IdadeMinima")

    assert repr(politica) == repr(new_politica)

