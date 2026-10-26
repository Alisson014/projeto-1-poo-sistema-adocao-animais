import json
from pathlib import Path

from ..domain import Pessoa, Adotante
from ..domain.exceptions import NaoCadastradoError


class PessoaRespository:
    """Classe para manipulação de arquivos json referentes ao domínio de Pessoa
    
    A classe consegue manipular cada um dos bancos de cada subclasse de pessoa, sendo que
    as subclasses devem obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        animal_class (Adotante): subclasse considerada
    """

    def __init__(self, path, class_name:type[Adotante]):
        self.path = Path(path)
        self.class_name = class_name

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def create(self, pessoa: Pessoa):
        pessoas:dict = self.__get_data()
        # Verifica se o email já não está cadastrado
        if pessoas.get(pessoa.email):
            raise Exception(f"O email {pessoa.email} já está cadastrado no sistema")
        
        with self.path.open('w', encoding='utf-8') as file:
            pessoas[pessoa.email] = pessoa.to_dict()

            json.dump(pessoas, file, ensure_ascii=False, indent=4)
            return True

    def get_all(self):
        pessoas = self.__get_data()

        if not pessoas:
            return []

        return [self.class_name.from_dict(pessoas[email]) for email in pessoas.keys()]

    def get_by_email(self, email:str) -> Adotante:
        pessoas = self.__get_data()

        if not pessoas:
            raise NaoCadastradoError(email, "adotante")

        if not pessoas.get(email):
            raise NaoCadastradoError(email, "adotante")

        return self.class_name.from_dict(pessoas[email])

    def update(self, new_pessoa:Adotante):
        pessoas = self.__get_data()
        if not pessoas.get(new_pessoa.email):
            raise NaoCadastradoError(new_pessoa.email, "adotante")
        
        with self.path.open('w', encoding='utf-8') as file:

            pessoas[new_pessoa.email] = new_pessoa.to_dict()

            json.dump(pessoas, file, ensure_ascii=False, indent=4)

    def delete_by_email(self, email:str):
        pessoas = self.__get_data()
        if not pessoas.get(email):
            raise NaoCadastradoError(email, "adotante")
        
        with self.path.open('w', encoding='utf-8') as file:
            pessoas.pop(email)

            json.dump(pessoas, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator:bool=False):
        # validator previne invocações por engano
        if not validator:
            raise Exception("Operação não confirmada")
        
        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)