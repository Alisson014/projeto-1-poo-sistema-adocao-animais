
from ..domain.models.animal import Animal, Cachorro, Calopsita, Coelho, Gato

def build_animal(animal:dict) -> Animal | None:
    if animal.get("passeios_necessarios_dia") is not None:
        return Cachorro.from_dict(animal)
    elif animal.get("canta") is not None:
        return Calopsita.from_dict(animal)
    elif animal.get("tamanho_gaiola_m3") is not None:
        return Coelho.from_dict(animal)
    elif animal.get("independencia") is not None:
        return Gato.from_dict(animal)
    return None 
