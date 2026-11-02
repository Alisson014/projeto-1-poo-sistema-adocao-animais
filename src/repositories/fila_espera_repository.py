import json
from pathlib import Path
from datetime import datetime

from ..config import PesosCompatibilidade
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

        # Garante que o animal existe no banco
        # Levanta um NaoCadastradoError se não existir
        self.animal_repository.get_by_id(fila_espera.animal.id)
        
        filas[str(fila_espera.animal.id)] = fila_espera.to_dict()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(filas, file, ensure_ascii=False, indent=4)
        
        return True

    def get_all(self, pesos:PesosCompatibilidade):
        filas = self.__get_data()

        if not filas:
            return []

        res = []

        for i in filas.keys():
            try:
                fila = self.get_by_animal_id(i, pesos)

                # Só é adicionada à saída se for válida
                res.append(fila)
            except NaoCadastradoError:
                # Ignora os erros lançados por remoçam de filas
                pass

        return res
        

    def get_by_animal_id(self, animal_id, pesos: PesosCompatibilidade):
        filas = self.__get_data()

        if not filas.get(str(animal_id)):
            raise NaoCadastradoError(f"FilaEspera({animal_id})", self.path.__str__())

        fila = filas[str(animal_id)]

        entradas = []
        need_update = False
        for en in fila["fila"]:
            try:
                en["adotante"] = self.adotante_repository.get_by_email(en["adotante"])
                
                entrada = EntradaFila(**en)
                now = datetime.now()
                expirada = False

                if entrada.data_expiracao.year < now.year:
                    expirada = True
                elif entrada.data_expiracao.year == now.year:
                    if entrada.data_expiracao.month < now.month:
                        expirada = True
                    elif entrada.data_expiracao.month == now.month:
                        if entrada.data_expiracao.day < now.day:
                            expirada = True

                if expirada:
                    raise NaoCadastradoError(f"Entrada - {repr(entrada)}", self.path.__str__())    
                
                # Apenas entradas com adotante existente são consideradas
                # As demais são limpas por não serem salvas
                
                entradas.append(entrada)
            except NaoCadastradoError:
                need_update = True


        fila["fila"] = entradas

        try:
            animal = self.animal_repository.get_by_id(fila["animal"])
            fila["animal"] = animal
        except NaoCadastradoError:
            self.delete_by_animal_id(animal_id)
            raise NaoCadastradoError(f"FilaEspera removida por questões de integridade({animal_id})", self.path.__str__())

        res = FilaEspera(**fila, pesos=pesos)

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
