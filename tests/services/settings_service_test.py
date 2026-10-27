from src.config import Politica, DuracaoReserva, IdadeMinima, PesosCompatibilidade, PorteXArea
from src.services import PoliticaService
from src.domain.exceptions import NaoCadastradoError

from datetime import datetime
import pytest

path = "tests/data/settings.json"

porte_x_area = PorteXArea(nome="porte x area", data_modificacao=datetime.now(), porte_p_min=20, porte_m_min=40, porte_g_min=60)
pesos_compatibilidade = PesosCompatibilidade(nome="pesos compatibilidade", data_modificacao=datetime.now(), peso_porte_moradia=0.2, peso_experiencia_temperamento=0.3, peso_tempo_livre_energia=0.2, peso_criancas_temperamento=0.3)
duracao_reserva = DuracaoReserva(nome="duração reserva", data_modificacao=datetime.now(), duracao_dias=14)
idade_minima = IdadeMinima(nome="idade mínima", data_modificacao=datetime.now(), idade_minima=18)

politica_service = PoliticaService(path)

# A intenção deste teste é limpar automaticamente settings.json para evitar erros na criação de políticas já existentes
def test_delete_all():
    politica_service.delete_all()

def test_create_PorteXArea():
    assert politica_service.create("PorteXArea", porte_x_area.to_dict())

def test_create_PesosCompatibilidade():
    assert politica_service.create("PesosCompatibilidade", pesos_compatibilidade.to_dict())

def test_create_DuracaoReserva():
    assert politica_service.create("DuracaoReserva", duracao_reserva.to_dict())

def test_create_IdadeMinima():
    assert politica_service.create("IdadeMinima", idade_minima.to_dict())

def test_get_all():
    politicas = politica_service.get_all()

    for i in politicas:
        assert isinstance(i, Politica)

def test_get_by_name_PorteXArea():
    politica = politica_service.get_by_name("PorteXArea")
    assert isinstance(politica, PorteXArea)
    assert repr(politica) == repr(porte_x_area)

def test_get_by_name_PesosCompatibilidade():
    politica = politica_service.get_by_name("PesosCompatibilidade")
    assert isinstance(politica, PesosCompatibilidade)
    assert repr(politica) == repr(pesos_compatibilidade)

def test_get_by_name_DuracaoReserva():
    politica = politica_service.get_by_name("DuracaoReserva")
    assert isinstance(politica, DuracaoReserva)
    assert repr(politica) == repr(duracao_reserva)

def test_get_by_name_IdadeMinima():
    politica = politica_service.get_by_name("IdadeMinima")
    assert isinstance(politica, IdadeMinima)
    assert repr(politica) == repr(idade_minima)

def test_update_PorteXArea():
    politica = politica_service.get_by_name("PorteXArea")

    politica.porte_g_min = 100
    politica_service.update("PorteXArea", politica.to_dict())

    new_politica = politica_service.get_by_name("PorteXArea")

    assert repr(politica) == repr(new_politica)

def test_update_PesosCompatibilidade():
    politica = politica_service.get_by_name("PesosCompatibilidade")

    politica.nome = "Pesos compatibilidade"
    politica_service.update("PesosCompatibilidade", politica.to_dict())

    new_politica = politica_service.get_by_name("PesosCompatibilidade")

    assert repr(politica) == repr(new_politica)

def test_update_DuracaoReserva():
    politica = politica_service.get_by_name("DuracaoReserva")

    politica.duracao_dias = 15
    politica_service.update("DuracaoReserva", politica.to_dict())

    new_politica = politica_service.get_by_name("DuracaoReserva")

    assert repr(politica) == repr(new_politica)

def test_update_IdadeMinima():
    politica = politica_service.get_by_name("IdadeMinima")

    politica.nome = "Idade mínima"
    politica_service.update("IdadeMinima", politica.to_dict())

    new_politica = politica_service.get_by_name("IdadeMinima")

    assert repr(politica) == repr(new_politica)

def test_delete_by_name():
    politica_service.delete_by_name("IdadeMinima")

    with pytest.raises(NaoCadastradoError):
        politica_service.get_by_name("IdadeMinima")

    # Apenas para questões de consulta aos dados persistidos
    politica_service.create("IdadeMinima", idade_minima.to_dict())
