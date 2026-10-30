
from pathlib import Path

class AnimalPath:
    # Garante que a pasta exista
    Path("data/animal").mkdir(parents=True, exist_ok=True)

    cachorro = "data/animal/cachorro.json"
    calopsita = "data/animal/calopsita.json"
    coelho = "data/animal/coelho.json"
    gato = "data/animal/gato.json"
