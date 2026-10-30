from src.domain.models.animal import Animal
from src.domain.models.pessoa import Adotante
from src.config import PesosCompatibilidade
from src.domain.enums import Moradia, Porte, Temperamento, Experiencia, Energia

def get_compatibilidade_porte(animal:Animal, adotante: Adotante):
    matriz_compatibilidade = {
        (Porte.G.value, Moradia.CASA_COM_QUINTAL.value): 100.0,
        (Porte.G.value, Moradia.CASA_COM_QUINTAL.value): 70.0,
        (Porte.G.value, Moradia.APARTAMENTO_COM_VARANDA.value): 40.0,
        (Porte.G.value, Moradia.APARTAMENTO_SEM_VARANDA.value): 20.0,

        (Porte.M.value, Moradia.CASA_COM_QUINTAL.value): 100.0,
        (Porte.M.value, Moradia.CASA_SEM_QUINTAL.value): 90.0,
        (Porte.M.value, Moradia.APARTAMENTO_COM_VARANDA.value): 80.0,
        (Porte.M.value, Moradia.APARTAMENTO_SEM_VARANDA.value): 60.0,
        
        (Porte.P.value, Moradia.CASA_COM_QUINTAL.value): 100.0,
        (Porte.P.value, Moradia.CASA_SEM_QUINTAL.value): 100.0,
        (Porte.P.value, Moradia.APARTAMENTO_COM_VARANDA.value): 100.0,
        (Porte.P.value, Moradia.APARTAMENTO_SEM_VARANDA.value): 90.0,
    }

    key = (animal.porte, adotante.moradia)

    return matriz_compatibilidade.get(key, 50)

def get_compatibilidade_experiencia_temperamento(animal: Animal, adotante:Adotante):
    matriz_compatibilidade = {
        (Temperamento.ARISCO.value, Experiencia.AVANCADO.value): 100.0,
        (Temperamento.ARISCO.value, Experiencia.INTERMEDIARIO.value): 70.0,
        (Temperamento.ARISCO.value, Experiencia.INICIANTE.value): 40.0,
        
        (Temperamento.MEDROSO.value, Experiencia.AVANCADO.value): 100.0,
        (Temperamento.MEDROSO.value, Experiencia.INTERMEDIARIO.value): 80.0,
        (Temperamento.MEDROSO.value, Experiencia.INICIANTE.value): 60.0,
        
        (Temperamento.DOCIL.value, Experiencia.AVANCADO.value): 100.0,
        (Temperamento.DOCIL.value, Experiencia.INTERMEDIARIO.value): 90.0,
        (Temperamento.DOCIL.value, Experiencia.INICIANTE.value): 80.0,
    }

    res = 0.0

    for temp in animal.temperamento:
        key = (temp.value, adotante.experiencia)
        res += matriz_compatibilidade.get(key, 50)

    return round(res/len(animal.temperamento), 2)

def get_compatibilidade_tempo_livre_energia(animal:Animal, adotante: Adotante):
    matriz_energia_tempo = {
        Energia.CALMO.value: 60,
        Energia.HIPERATIVO.value: 240,
    }

    tempo_necessario = matriz_energia_tempo[animal.energia]

    if adotante.tempo_livre_min >= tempo_necessario:
        return 100

    razao = adotante.tempo_livre_min / tempo_necessario
    return round(razao*100, 2)

def get_compatibilidade_criancas_temperamento(animal:Animal, adotante:Adotante):

    if not adotante.possui_criancas:
        return 100.0
    
    matriz_compatibilidade = {
        Temperamento.DOCIL.value: 100.0,
        Temperamento.MEDROSO.value: 60.0,
        Temperamento.ARISCO.value: 20,
    }
    res = 0.0
    for temp in animal.temperamento:
        res += matriz_compatibilidade[temp.value]

    return round( res / len(animal.temperamento), 2 )

def get_compatibilidade(animal:Animal, adotante:Adotante, pesos:PesosCompatibilidade) -> float:
    res = 0
    res += pesos.peso_porte_moradia * get_compatibilidade_porte(animal, adotante)
    res += pesos.peso_experiencia_temperamento * get_compatibilidade_experiencia_temperamento(animal, adotante)
    res += pesos.peso_tempo_livre_energia * get_compatibilidade_tempo_livre_energia(animal, adotante)
    res += pesos.peso_criancas_temperamento * get_compatibilidade_criancas_temperamento(animal, adotante)

    return res