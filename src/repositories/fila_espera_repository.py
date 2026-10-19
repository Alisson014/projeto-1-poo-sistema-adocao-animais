import json
from pathlib import Path

from ..domain import FilaEspera, EntradaFila, Adotante
from ..domain.exceptions import NaoCadastradoError
from .animal_repository import AnimalRepository
from .pessoa_repository import PessoaRespository

class FilaEsperaRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de FilaEspera
        
    A classe consegue manipular cada um dos bancos de cada subclasse de fila_espera, sendo que
    as subclasses devem obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        animal_class_name: Classe do animal considerado
    """

    def __init__(self, path, animal_class_name, animal_path, adotante_path):
        self.path = Path(path)
        self.animal_repository = AnimalRepository(animal_path, animal_class_name)
        self.adotante_repository = PessoaRespository(adotante_path, Adotante)

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def create(self, fila_espera:FilaEspera):
        filas:dict = self.__get_data()

        if filas.get(str(fila_espera.animal.id)):
            raise Exception(f"({fila_espera.animal.__str__()}) já possui uma fila de espera")

        try:
            self.animal_repository.get_by_id(fila_espera.animal.id)
        except NaoCadastradoError:
            raise Exception(f"({fila_espera.animal.__str__()}) não cadastrado no banco")

        filas[str(fila_espera.animal.id)] = fila_espera.to_dict()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(filas, file, ensure_ascii=False, indent=4)
        
        return True

    def get_all(self):
        filas = self.__get_data()

        if not filas:
            return []

        res = []

        try:
            for i in filas.keys():
                fila = self.get_by_animal_id(i)

                # Só é adicionada à saída se for válida
                res.append(fila)
        except NaoCadastradoError:
            # Ignora os erros lançados por remoçam de filas
            pass

        return res
        

    def get_by_animal_id(self, animal_id):
        filas = self.__get_data()

        if not filas.get(str(animal_id)):
            raise NaoCadastradoError(f"FilaEspera({animal_id})", self.path.__str__())

        fila = filas[str(animal_id)]

        entradas = []
        need_update = False
        for en in fila["fila"]:
            try:
                en["adotante"] = self.adotante_repository.get_by_email(en["adotante"])

                # Apenas entradas com adotante existente são consideradas
                # As demais são limpas por não serem salvas
                entradas.append(EntradaFila.from_dict(en))
            except NaoCadastradoError:
                need_update = True


        fila["fila"] = entradas

        try:
            animal = self.animal_repository.get_by_id(fila["animal"])
            fila["animal"] = animal
        except NaoCadastradoError:
            self.delete_by_animal_id(animal_id)
            raise NaoCadastradoError(f"FilaEspera removida por questões de integridade({animal_id})", self.path.__str__())

        res = FilaEspera.from_dict(fila)

        # Espelha a limpeza dos dados no banco
        if need_update:
            self.update(res)
        
        return res

    def update(self, new_fila:FilaEspera):
        filas = self.__get_data()

        if not filas.get(str(new_fila.animal.id)):
            raise NaoCadastradoError(f"FilaEspera({new_fila.animal.id})", self.path.__str__())

        filas[str(new_fila.animal.id)] = new_fila.to_dict()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(filas, file, ensure_ascii=False, indent=4)

    def delete_by_animal_id(self, animal_id):
        filas = self.__get_data()
        
        if not filas.get(str(animal_id)):
            raise NaoCadastradoError(f"FilaEspera({animal_id})", self.path.__str__())

        filas.pop(str(animal_id))

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(filas, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator:bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
