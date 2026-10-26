from ..domain import Adotante, Pessoa
from ..repositories import PessoaRespository, PoliticaRepository
from ..config import IdadeMinima
from ..domain.exceptions import PoliticaError

from typing import Literal

class PessoaService:
    """Classe para modelar os serviços referentes ao domínio de pessoa

    A classe é responsável pro garantir o cumprimento das regras de negócio 
    e a utilização dos repositories

    Attributes:
        repository (dict[str, PessoaRespository]): Mapeamento dos repositories disponíveis no domínio
        class_initializer (dict[str, type[Adotante]]): Mapeamento das subclasses de Pessoa
    """
    def __init__(self, adotante_path:str, politica_path):
        self.repository: dict[str, PessoaRespository] = {
            "Adotante": PessoaRespository(adotante_path, Adotante)
        }
        self.class_initializer: dict[str, type[Pessoa]] = {
            "Adotante": Adotante
        }
        self.Politica: IdadeMinima = PoliticaRepository(politica_path).get_by_name("IdadeMinima")

    def create(self, type_pessoa: Literal["Adotante"], pessoa_data:dict):
        model = self.class_initializer[type_pessoa]
        repo = self.repository[type_pessoa]

        # Instancia classe model
        # As exceções de validação são lançadas pela classe model
        pessoa = model(**pessoa_data)

        if not self.Politica.validar(pessoa.idade):
            raise PoliticaError(type(self.Politica).__name__)

        repo.create(pessoa)

        return pessoa

    def get_all(self):
        res:list[Pessoa] = []
        repo = self.repository["Adotante"]

        res.extend( repo.get_all() )

        return res

    def get_by_email(self, type_pessoa: Literal["Adotante"], email:str):
        repo = self.repository[type_pessoa]
        pessoa = repo.get_by_email(email)

        return pessoa

    def update(self, type_pessoa: Literal["Adotante"], updated_data:dict, email:str):
        repo = self.repository[type_pessoa]

        updated_pessoa = repo.get_by_email(email)
        # Realiza a atualização dos dados da pessoa
        # Como há validação na classe, as exceptions serão disparadas pela classe.
        for key, value in updated_data.items():
            if hasattr(updated_pessoa, key) and key != "email" and key != "idade":
                setattr(updated_pessoa, key, value)

        if updated_data.get("idade"):
            if not self.Politica.validar(updated_data["idade"]):
                raise PoliticaError(type(self.Politica).__name__)

            updated_pessoa.idade = updated_data["idade"]

        repo.update(updated_pessoa)
        return updated_pessoa

    def delete_by_email(self, type_pessoa: Literal["Adotante"], email:str):
        repo = self.repository[type_pessoa]
        repo.delete_by_email(email)

    def delete_all(self, type_pessoa: Literal["Adotante"]):
        repo = self.repository[type_pessoa]
        repo.delete_all(True)
