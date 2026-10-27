from ..domain import Animal, Cachorro, Calopsita, Coelho, Gato, Quarentena
from ..repositories import QuarentenaRepository

from typing import Literal


class QuarentenaService:
    """Classe para modelar os serviços referentes ao domínio de quarentena

    A classe é responsável pro garantir o cumprimento das regras de negócio 
    e a utilização dos repositories

    Attributes:
        repository (dict[str, QuarentenaRepository]): Mapeamento dos repositories disponíveis no domínio
        class_initializer (dict[str, type[Animal]]): Mapeamento das subclasses de Animal
    """
    def __init__(
            self, 
            path_q_cach:str, 
            path_q_cal:str, 
            path_q_co:str, 
            path_q_ga:str,
            path_cach:str,
            path_cal:str,
            path_co:str,
            path_ga:str
        ):
        self.repository: dict[str, QuarentenaRepository] = {
            "Cachorro": QuarentenaRepository(path_q_cach, Cachorro, path_cach),
            "Calopsita": QuarentenaRepository(path_q_cal, Calopsita, path_cal),
            "Coelho": QuarentenaRepository(path_q_co, Coelho, path_co),
            "Gato": QuarentenaRepository(path_q_ga, Gato, path_ga),
        }
        
        # Instanciador de classes model
        self.class_initializer: dict[str, type[Animal]] = {
            "Cachorro": Cachorro,
            "Calopsita": Calopsita,
            "Coelho": Coelho,
            "Gato": Gato
        }

    def create(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], quarentena_data:dict):
        model = self.class_initializer[type_animal]
        repo = self.repository[type_animal]

        quarentena_data["animal"] = model.from_dict(quarentena_data["animal"])

        # Instancia classe model
        # As exceções de validação são lançadas pela classe model
        quarentena:Quarentena = Quarentena(**quarentena_data, id=repo.generate_id())

        repo.create(quarentena)

        return quarentena

    def get_all(self):
        res: list[Quarentena] = []
        for repo in self.repository.values():
            res.extend(repo.get_all())

        return res

    def get_all_type_animal(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]):
        repo = self.repository[type_animal]
        return repo.get_all()

    def get_by_id(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], id:int):
        repo = self.repository[type_animal]
        return repo.get_by_id(id)

    def update(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], updated_data:dict, id:int):
        repo = self.repository[type_animal]

        updated_quarentena = repo.get_by_id(id)

        # Realiza a atualização dos dados do animal
        # A regra de negócio do status é implementada via setter
        # Como há validação na classe, as exceptions serão disparadas pela classe.
        for key, value in updated_data.items():
            if hasattr(updated_quarentena, key) and key != "id" and key != "animal":
                setattr(updated_quarentena, key, value)

        repo.update(updated_quarentena)
        return updated_quarentena

    def delete_by_id(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"], id:int):
        repo = self.repository[type_animal]
        repo.delete_by_id(id)

    def delete_all(self, type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]):
        repo = self.repository[type_animal]
        repo.delete_all(True)
