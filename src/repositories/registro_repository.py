import json
from pathlib import Path

from ..domain import Adocao, Devolucao, Reserva, Adotante
from ..domain.exceptions import NaoCadastradoError
from .animal_repository import AnimalRepository
from .pessoa_repository import PessoaRespository

class RegistroRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de Registro
    
    A classe consegue manipular cada um dos bancos de registro, sendo que
    a classe deve obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        class_name: Subclasse do registro considerado
    """

    def __init__(self, path, class_name, animal_path, animal_class_name, adotante_path):
        self.path = Path(path)
        self.class_name: type[Adocao | Devolucao | Reserva] = class_name
        self.animal_repository = AnimalRepository(animal_path, animal_class_name)
        self.adotante_repository = PessoaRespository(adotante_path, Adotante)

    def generate_id(self):
        registros = self.__get_data()

        if not registros:
            return 1

        return max(int(id) for id in registros.keys()) +1

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def create(self, registro: Adocao | Devolucao | Reserva):
        registros = self.__get_data()

        if registros.get(str(registro.id)):
            raise Exception(f"O id {registro.id} já está reservado para um registro")

        with self.path.open('w', encoding='utf-8') as file:
            registros[registro.id] = registro.to_dict()

            json.dump(registros, file, ensure_ascii=False, indent=4)

        return True
        

    def get_all(self):
        registros = self.__get_data()

        if not registros:
            return []

        res = []
        ids_inexistentes = []
        # busca os animais referentes ao id armazenado
        for i in registros.keys():
            try:
                registros[i]["animal"] = self.animal_repository.get_by_id(registros[i]["animal"])
                registros[i]["adotante"] = self.adotante_repository.get_by_email(registros[i]["adotante"])

                res.append(self.class_name.from_dict(registros[i]))
            except NaoCadastradoError:
                # Ignora caso o código tente buscar o id de um animal que foi deletado
                # Precaução a falhas na consistência dos dados
                ids_inexistentes.append(i)

        # Limpa as quarentenas inválidas do sistema
        for i in ids_inexistentes:
            self.delete_by_id(i)

        return res

    def get_by_id(self, id):
        registros = self.__get_data()

        if not registros.get(str(id)):
            raise NaoCadastradoError(f"Registro({id})", self.path.__str__())

        registro = registros[str(id)]
        try:
            registro["animal"] = self.animal_repository.get_by_id(registro["animal"])
            registro["adotante"] = self.adotante_repository.get_by_email(registro["adotante"])
        except NaoCadastradoError:
            # Limpa a quarentena inválida da memória
            self.delete_by_id(id)
            raise NaoCadastradoError(f"Quarentena({id})", self.path.__str__())

        return self.class_name.from_dict(registro)

    def update(self, new_registro:Adocao | Devolucao | Reserva):
        registros = self.__get_data()

        if not registros.get(str(new_registro.id)):
            raise NaoCadastradoError(f"Quarentena({new_registro.id})", self.path.__str__())

        with self.path.open('w', encoding='utf-8') as file:
            registros[str(new_registro.id)] = new_registro.to_dict()

            json.dump(registros, file, ensure_ascii=False, indent=4)

    def delete_by_id(self, id):
        registros = self.__get_data()

        if not registros.get(str(id)):
            raise NaoCadastradoError(f"Registro({id})", self.path.__str__())

        with self.path.open('w', encoding='utf-8') as file:
            registros.pop(str(id))

            json.dump(registros, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator:bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
