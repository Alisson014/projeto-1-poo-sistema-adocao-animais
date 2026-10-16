import json
from pathlib import Path
from datetime import datetime

from ..domain.models import Quarentena
from ..domain.exceptions import NaoCadastradoError, NaoEncontradoError
from .animal_repository import AnimalRepository


class QuarentenaRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de Quarentena
    
    A classe consegue manipular cada um dos bancos de quarentena, sendo que
    a classe deve obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        class_name: Subclasse do animal considerado
        animal_path: caminho do arquivo json para as quarentenas do tipo animal considerado
        animal_repository: AnimalRepository
    """

    def __init__(self, path, class_name, animal_path):
        self.path = Path(path)
        self.animal_repository: AnimalRepository = AnimalRepository(animal_path, class_name)

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def generate_id(self) -> int:
        quarentenas = self.__get_data()

        # O primeiro id é sempre 1
        if not quarentenas:
            return 1

        #retorna o incremento do último id
        return max(int(id) for id in quarentenas.keys()) + 1
        

    def create(self, quarentena:Quarentena):
        quarentenas = self.__get_data()

        for i in quarentenas.keys():
            if quarentenas[i]["animal"] == str(quarentena.animal.id):
                if quarentenas[i]["status"] == "ATIVA":
                    raise Exception("Um animal não pode cumprir duas quarentenas ao mesmo tempo")
                break

        with self.path.open('w', encoding='utf-8') as file:
            quarentenas[quarentena.id] = quarentena.to_dict()

            json.dump(quarentenas, file, ensure_ascii=False, indent=4)
            return True

    def get_all(self):
        quarentenas = self.__get_data()

        if not quarentenas:
            return []

        res = []
        ids_inexistentes = []
        # busca os animais referentes ao id armazenado
        for i in quarentenas.keys():
            try:
                quarentenas[i]["animal"] = self.animal_repository.get_by_id(quarentenas[i]["animal"])

                formater = Quarentena(
                        id= 0, animal=quarentenas[i]["animal"], data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
                )

                res.append(formater.from_dict(quarentenas[i]))
            except NaoCadastradoError:
                # Ignora caso o código tente buscar o id de um animal que foi deletado
                # Precaução a falhas na consistência dos dados
                ids_inexistentes.append(i)

        # Limpa as quarentenas inválidas do sistema
        for i in ids_inexistentes:
            self.delete_by_id(i)

        return res

    def get_by_id(self, id:int):
        quarentenas = self.__get_data()

        if not quarentenas:
            return None

        quarentena = quarentenas[str(id)]

        try:
            quarentena["animal"] = self.animal_repository.get_by_id(quarentena["animal"])
        except NaoCadastradoError:
            # Limpa a quarentena inválida da memória
            self.delete_by_id(id)

            raise NaoEncontradoError(f"Quarentena({id})")

        formater = Quarentena(
            id= 0, animal=quarentena["animal"], data_inicial=datetime.now(), motivo="OUTRO", status="CUMPRIDA"
        )

        return formater.from_dict(quarentena)

    def update(self, new_quarentena:Quarentena):
        quarentenas = self.__get_data()

        if not quarentenas.get(str(new_quarentena.id)):
            raise NaoCadastradoError(f"Quarentena({new_quarentena.id})", self.path.__str__())

        with self.path.open('w', encoding='utf-8') as file:
            quarentenas[str(new_quarentena.id)] = new_quarentena.to_dict()

            json.dump(quarentenas, file, ensure_ascii=False, indent=4)


    def delete_by_id(self, id: int):
        quarentenas = self.__get_data()

        if not quarentenas.get(str(id)):
            raise NaoEncontradoError(f"Quarentena({id})")

        with self.path.open('w', encoding='utf-8') as file:

            quarentenas.pop(str(id))

            json.dump(quarentenas, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator:bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)

    