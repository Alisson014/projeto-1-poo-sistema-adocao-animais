import json
from ..domain import Animal, Cachorro, Calopsita, Coelho, Gato, Evento, Vacina
from pathlib import Path


class AnimalRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de Animal

    A classe consegue manipular cada um dos bancos de cada subclasse de animal, sendo que
    as subclasses devem obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        animal_class (Cachorro | Calopsita | Coelho | Gato): subclasse considerada
    """

    def __init__(self, path, animal_class: Cachorro | Calopsita | Coelho | Gato):
        self.path = Path(path)
        self.animal_class = animal_class

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return {}

    def create(self, animal: Animal):
        animais: dict = self.__get_data()
        with self.path.open("w", encoding="utf-8") as file:
            # As chaves no json são strings, é preciso converter o id para str
            if animais.get(str(animal.id)):
                raise Exception(f"O id {animal.id} já está reservado para um animal")

            animais[str(animal.id)] = animal.to_dict()

            json.dump(animais, file, ensure_ascii=False, indent=4)
            return True

    def get_all(self) -> list[Animal]:
        # Retorna uma lista vazia se o arquivo não existir
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            animais: dict = json.load(file)

            if not animais:
                return []

            # Converte os eventos em instâncias
            for i in animais.keys():
                for d in animais[i]["historico"]:
                    print(d)
                    d = Evento.from_dict(d)

            res = [self.animal_class.from_dict(animais[id]) for id in animais.keys()]

            return res

    def get_by_id(self, id: int) -> Animal | None:
        # Retorna None caso o arquivo não exista
        if not self.path.exists():
            return None

        with self.path.open("r", encoding="utf-8") as file:
            animais: dict = json.load(file)

            # Levanta uma exceção caso o id não exista
            if not animais.get(str(id)):
                raise Exception(f"{id} não existente no banco de animais")

            animal = animais[str(id)]

            for d in animal["historico"]:
                d = Evento.from_dict(d)

            if animal.get("vacinas"):
                for d in animal["vacinas"]:
                    d = Vacina.from_dict(d)

            return self.animal_class.from_dict(animal)

    def update(self, new_animal: Animal):
        animais: dict = self.__get_data()

        with self.path.open("w", encoding="utf=8") as file:
            if not animais.get(str(new_animal.id)):
                raise Exception(f"O id {new_animal.id} não existe no banco de animais")

            animais[str(new_animal.id)] = new_animal.to_dict()

            json.dump(animais, file, ensure_ascii=False, indent=4)

    def delete_by_id(self, id):
        animais = self.__get_data()

        with self.path.open("w", encoding="utf-8") as file:
            if not animais.get(str(id)):
                raise Exception(f"O id {id} não existe no banco de animais")

            # Remove o item cuja chave é o id passado como parâmetro
            animais.pop(str(id))

            json.dump(animais, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator: bool = False):
        with self.path.open("w", encoding="utf-8") as file:
            # Validator previne invacações por engano
            if not validator:
                raise Exception("Operação não validada")

            json.dump({}, file, ensure_ascii=False, indent=4)

    def id_generate(self):
        try:
            animais = self.__get_data()
        except Exception:
            # Ignora se erros ocorrerem caso o arequivo não exista
            pass

        # O primeiro id é sempre 1
        if not animais:
            return 1

        # Retorna o incremento do último id
        return max(int(id) for id in animais.keys()) + 1
