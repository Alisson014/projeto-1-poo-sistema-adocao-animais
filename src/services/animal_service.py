from ..domain import Animal, Cachorro, Calopsita, Coelho, Gato, Vacina, Evento
from ..repositories import AnimalRepository

from typing import Literal


class AnimalService:
    """Classe para modelar os serviços referentes ao domínio de animal

    A classe é responsável pro garantir o cumprimento das regras de negócio 
    e a utilização dos repositories

    Attributes:
        repository (dict[str, AnimalRepository]): Mapeamento dos repositories disponíveis no domínio
        class_initializer (dict[str, type[Animal]]): Mapeamento das subclasses de Animal
    """

    def __init__(self, cachorro_path:str, calopsita_path:str, coelho_path:str, gato_path:str):
        # Mapeia os tipos de animais aos seus respectivos repositórios
        self.repository: dict[str, AnimalRepository] = {
            "Cachorro": AnimalRepository(cachorro_path, Cachorro),
            "Calopsita": AnimalRepository(calopsita_path, Calopsita),
            "Coelho": AnimalRepository(coelho_path, Coelho),
            "Gato": AnimalRepository(gato_path, Gato)
        }

        # Instanciador de classes model
        self.class_initializer: dict[str, type[Animal]] = {
            "Cachorro": Cachorro,
            "Calopsita": Calopsita,
            "Coelho": Coelho,
            "Gato": Gato
        }

    def create(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], animal_data:dict):
        model = self.class_initializer[type_animal]
        repo = self.repository[type_animal]
        
        # Instancia classe model
        # As exceções de validação são lançadas pela classe model
        animal:Animal = model(**animal_data, id=repo.generate_id())

        repo.create(animal)

        return animal

    def get_all(self):
        res:list[Animal] = []
        for repo in self.repository.values():
            res.extend(repo.get_all())

        return res

    def get_all_type_animal(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]):
        repo = self.repository[type_animal]

        return repo.get_all()

    def get_by_id(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], id:int):
        repo = self.repository[type_animal]

        return repo.get_by_id(id)

    def update(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], animal_data:dict, animal_id:int):
        repo = self.repository[type_animal]

        updated_animal: Animal = repo.get_by_id(int(animal_id))

        # Realiza a atualização dos dados do animal
        # A regra de negócio do status é implementada via setter
        # Como há validação na classe, as exceptions serão disparadas pela classe.
        for key, value in animal_data.items():
            if hasattr(updated_animal, key) and key != "id" and key != "vacinas" and key != "historico":
                setattr(updated_animal, key, value)

        if animal_data.get("vacinas") is not None:
            for va in (animal_data["vacinas"]):
                vacina = Vacina.from_dict(va)
                if not vacina in updated_animal.get_vacinas(): # type: ignore[attr-defined, union-attr]
                    updated_animal.vacinar(vacina) # type: ignore[attr-defined, union-attr]

        # Tratamento da atualização de eventos
        if animal_data.get("historico"):
            new_eventos = []
            for ev in animal_data["historico"]:
                new_eventos.append(Evento.from_dict(ev))
            
            eventos_cad = []
            for cad_ev in updated_animal.get_historico():
                eventos_cad.append(Evento.from_dict(cad_ev))

            for evento in new_eventos:
                if not evento in eventos_cad:
                    updated_animal.adicionar_evento(evento)
            
            for evento in eventos_cad:
                if not evento in new_eventos:
                    updated_animal.remover_evento(evento)

        repo.update(updated_animal)
        return updated_animal

    def delete_by_id(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], id:int | str):
        repo = self.repository[type_animal]
        repo.delete_by_id(id)

    def delete_all(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]):
        repo = self.repository[type_animal]
        repo.delete_all(True)


