from ..domain import Registro, Reserva, Devolucao, Adocao
from ..domain import Cachorro, Calopsita, Coelho, Gato, Animal, Adotante
from ..config import PesosCompatibilidade
from ..repositories import RegistroRepository, PoliticaRepository
from ..domain.exceptions import PoliticaError

from typing import Literal
from datetime import timedelta

class RegistroService:
    """Classe para modelar os serviços referentes ao domínio de registro

    A classe é responsável pro garantir o cumprimento das regras de negócio 
    e a utilização dos repositories

    Attributes:
        repository (dict[str, RegistroRepository]): Mapeamento dos repositories disponíveis no domínio
        regis_class_initializer (dict[str, type[Registro]]): Mapeamento das subclasses de Registro
        animal_class_initializer (dict[str, type[Animal]]): Mapeamento das subclasses de Animal
        politica_path (Path): Caminho do json de política para inicialização do PoliticaRepository
    """
    def __init__(
            self,
            path_reserva_cacho:str,
            path_reserva_calop:str,
            path_reserva_coel:str,
            path_reserva_gato:str,
            path_devo_cacho:str,
            path_devo_calop:str,
            path_devo_coel:str,
            path_devo_gato:str,
            path_adocao_cacho:str,
            path_adocao_calop:str,
            path_adocao_coel:str,
            path_adocao_gato:str,
            cacho_path:str,
            calop_path:str,
            coel_path:str,
            gato_path:str,
            adotante_path:str,
            politica_path:str
        ):

        # Mapeia registros e as subdivisões entre os animais
        self.repository: dict[str, dict[str, RegistroRepository]] = {
            "Adocao": {
                "Cachorro": RegistroRepository(path_adocao_cacho, Adocao, cacho_path, Cachorro, adotante_path),
                "Calopsita": RegistroRepository(path_adocao_calop, Adocao, calop_path, Calopsita, adotante_path),
                "Coelho": RegistroRepository(path_adocao_coel, Adocao, coel_path, Coelho, adotante_path),
                "Gato": RegistroRepository(path_adocao_gato, Adocao, gato_path, Gato, adotante_path),
            },
            "Devolucao": {
                "Cachorro": RegistroRepository(path_devo_cacho, Devolucao, cacho_path, Cachorro, adotante_path),
                "Calopsita": RegistroRepository(path_devo_calop, Devolucao, calop_path, Calopsita, adotante_path),
                "Coelho": RegistroRepository(path_devo_coel, Devolucao, coel_path, Coelho, adotante_path),
                "Gato": RegistroRepository(path_devo_gato, Devolucao, gato_path, Gato, adotante_path),
            },
            "Reserva": {
                "Cachorro": RegistroRepository(path_reserva_cacho, Reserva, cacho_path, Cachorro, adotante_path),
                "Calopsita": RegistroRepository(path_reserva_calop, Reserva, calop_path, Calopsita, adotante_path),
                "Coelho": RegistroRepository(path_reserva_coel, Reserva, coel_path, Coelho, adotante_path),
                "Gato": RegistroRepository(path_reserva_gato, Reserva, gato_path, Gato, adotante_path),
            },
        }
        self.regis_class_initializer: dict[str, type[Adocao | Devolucao | Reserva]] = {
            "Adocao": Adocao,
            "Devolucao": Devolucao,
            "Reserva": Reserva,
        }
        self.animal_class_initializer: dict[str, type[Animal]] = {
            "Cachorro": Cachorro,
            "Calopsita": Calopsita,
            "Coelho": Coelho,
            "Gato": Gato
        }
        self.politica_repository = PoliticaRepository(politica_path)

    def create(
            self,
            type_registro: Literal["Adocao", "Devolucao", "Reserva"],
            type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
            registro_data: dict,
            Pesos: PesosCompatibilidade | None = None
            ):
        regis_model = self.regis_class_initializer[type_registro]
        animal_model = self.animal_class_initializer[type_animal]
        repo = self.repository[type_registro][type_animal]

        registro_data["animal"] = animal_model.from_dict(registro_data["animal"])
        registro_data["adotante"] = Adotante.from_dict(registro_data["adotante"])

        # O tratamento das exceções é feito pela classe model
        registro: Adocao | Devolucao | Reserva = regis_model(**registro_data, id=repo.generate_id())

        if isinstance(registro, Adocao):
            registro.taxa = registro.calcular_taxa()

        # Validação da política de área mínima para o porte do animal
        if isinstance(registro, Adocao) or isinstance(registro, Reserva):
            if not self.politica_repository.get_by_name("PorteXArea").validar(registro.animal.porte, registro.adotante.area_util):
                raise PoliticaError(f"Area útil do adotante abaixo da mínima para o porte {registro.animal.porte}")

        if isinstance(registro, Reserva):
            intervalo = timedelta(days=self.politica_repository.get_by_name("DuracaoReserva").duracao_dias)
            registro.data_expiracao = registro.data_inicial + intervalo

        if Pesos is None:
            Pesos: PesosCompatibilidade = self.politica_repository.get_by_name("PesosCompatibilidade")
        
        repo.create(registro, Pesos)
        return registro

    def get_all(self):
        """Retorna todos os registros, independentemente do tipo"""
        res: list[Registro] = []

        for repo_key in self.repository.keys():
            for repo in self.repository[repo_key].values():
                res.extend(repo.get_all())

        return res

    def get_all_type_registro(self, type_registro: Literal["Adocao", "Devolucao", "Reserva"]):
        res: list[Registro] = []
        
        for repo in self.repository[type_registro].values():
            res.extend(repo.get_all())

        return res

    def get_all_type_registro_type_animal(
            self,
            type_registro: Literal["Adocao", "Devolucao", "Reserva"],
            type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
        ):
        repo = self.repository[type_registro][type_animal]

        res: list[Registro] = repo.get_all()

        return res

    def get_by_id(
            self,
            type_registro: Literal["Adocao", "Devolucao", "Reserva"],
            type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
            id: int,
        ):
        repo = self.repository[type_registro][type_animal]

        registro = repo.get_by_id(id)

        return registro

    def update(
            self,
            type_registro: Literal["Adocao", "Devolucao", "Reserva"],
            type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
            registro_data: dict,
            id: int
        ):
        repo = self.repository[type_registro][type_animal]

        updated_registro = repo.get_by_id(id)

        # Realiza a atualização dos dados
        # As validações são feitas pela própria classe
        for key, value in registro_data.items():
            if hasattr(updated_registro, key) and key != "id" and key != "animal" and key != "adotante":
                setattr(updated_registro, key, value)

        repo.update(updated_registro)

        return updated_registro

    def delete_by_id(
            self,
            type_registro: Literal["Adocao", "Devolucao", "Reserva"],
            type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
            id: int
        ):
        repo = self.repository[type_registro][type_animal]
        repo.delete_by_id(id)

    def delete_all_registro(self, type_registro: Literal["Adocao", "Devolucao", "Reserva"]):
        for repo in self.repository[type_registro].values():
            repo.delete_all(True)
        
        
    def delete_all(self):
        for repo_key in self.repository.keys():
            for repo in self.repository[repo_key].values():
                repo.delete_all(True)
