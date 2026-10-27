# Declaro utilização de IA para geração do código abaixo
# IA utilizada: claude
# Tomei essa decisão em decorrência do pouco tempo que possuo para finalizar a entrega 4
# prompt:
"""
Continuação do chat utilizado em relatorio_service.py
"""


from ..domain import FilaEspera, Animal
from ..repositories import FilaEsperaRepository


class FilaEsperaService:
    """Classe para modelar os serviços referentes ao domínio de FilaEspera

    A classe é responsável por garantir o cumprimento das regras de negócio
    e a utilização dos repositories. Cada instância trabalha com a fila de espera
    de uma única subclasse de animal (Cachorro | Calopsita | Coelho | Gato)

    Attributes:
        repository (FilaEsperaRepository): Repository das filas de espera da subclasse considerada
        animal_repository (AnimalRepository): Repository dos animais da subclasse considerada
        adotante_repository (PessoaRespository): Repository dos adotantes
    """

    def __init__(self, path: str, animal_class: type[Animal], animal_path: str, adotante_path: str):
        self.repository = FilaEsperaRepository(path, animal_class, animal_path, adotante_path)
        self.animal_repository = self.repository.animal_repository
        self.adotante_repository = self.repository.adotante_repository

    def create(self, animal_id: int):
        # Levanta NaoCadastradoError se o animal não existir
        animal = self.animal_repository.get_by_id(int(animal_id))

        # Toda fila de espera é criada vazia
        fila = FilaEspera(animal=animal)

        self.repository.create(fila)

        return fila

    def get_all(self):
        return self.repository.get_all()

    def get_by_animal_id(self, animal_id: int):
        return self.repository.get_by_animal_id(animal_id)

    def add_adotante(self, animal_id: int, adotante_email: str):
        fila: FilaEspera = self.repository.get_by_animal_id(animal_id)

        # Levanta NaoCadastradoError se o adotante não existir
        adotante = self.adotante_repository.get_by_email(adotante_email)

        # As regras da fila (como a de adotante duplicado) são validadas pela classe model
        fila.add(adotante)

        self.repository.update(fila)
        return fila

    def remove_adotante(self, animal_id: int, adotante_email: str):
        fila: FilaEspera = self.repository.get_by_animal_id(animal_id)

        adotante = self.adotante_repository.get_by_email(adotante_email)

        # Levanta NaoEncontradoError se o adotante não estiver na fila
        fila.remove(adotante)

        self.repository.update(fila)
        return fila

    def proximo(self, animal_id: int):
        fila: FilaEspera = self.repository.get_by_animal_id(animal_id)

        # Retorna None se a fila estiver vazia
        return fila.proximo()

    def delete_by_animal_id(self, animal_id: int | str):
        self.repository.delete_by_animal_id(animal_id)

    def delete_all(self):
        self.repository.delete_all(True)