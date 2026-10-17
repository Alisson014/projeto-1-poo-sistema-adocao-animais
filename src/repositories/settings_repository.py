import json
from pathlib import Path

from ..config import IdadeMinima, DuracaoReserva, PesosCompatibilidade, PorteXArea
from ..domain.exceptions import NaoCadastradoError

class PoliticaRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de Politica
        
    A classe consegue manipular cada um dos bancos de politica, sendo que
    as subclasses devem obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        class_name: Subclasse de política considerada
    """

    def __init__(self, path):
        self.path = Path(path)

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def create(self, politica:IdadeMinima | DuracaoReserva | PesosCompatibilidade | PorteXArea):
        politicas = self.__get_data()

        if politicas.get(type(politica).__name__):
            raise Exception(f"politica de {type(politica).__name__} já cadastrada")

        with self.path.open('w', encoding='utf-8') as file:
            politicas[type(politica).__name__] = politica.to_dict()
            
            json.dump(politicas, file, ensure_ascii=False, indent=4)

        return True

    def get_all(self):
        politicas = self.__get_data()

        if not politicas:
            return []

        res = []

        for i in politicas.keys():
            match i:
                case "IdadeMinima":
                    res.append(IdadeMinima.from_dict(politicas[i]))
                case "DuracaoReserva":
                    res.append(DuracaoReserva.from_dict(politicas[i]))
                case "PesosCompatibilidade":
                    res.append(PesosCompatibilidade.from_dict(politicas[i]))
                case "PorteXArea":
                    res.append(PorteXArea.from_dict(politicas[i]))

        return res

    def get_by_name(self, name):
        politicas = self.__get_data()

        if not politicas.get(name):
            raise NaoCadastradoError(f"Politica({name})", self.path.__str__())

        politica = politicas[name]

        match name:
            case "IdadeMinima":
                politica = IdadeMinima.from_dict(politica)
            case "DuracaoReserva":
                politica = DuracaoReserva.from_dict(politica)
            case "PesosCompatibilidade":
                politica = PesosCompatibilidade.from_dict(politica)
            case "PorteXArea":
                politica = PorteXArea.from_dict(politica)
            case _:
                raise Exception("Política inválida")

        return politica

    def update(self, new_politica:IdadeMinima | DuracaoReserva | PesosCompatibilidade | PorteXArea):
        politicas = self.__get_data()

        with self.path.open('w', encoding='utf-8') as file:
            politicas[type(new_politica).__name__] = new_politica.to_dict()

            json.dump(politicas, file, ensure_ascii=False, indent=4)

    def delete_by_name(self, name):
        politicas = self.__get_data()

        if not politicas.get(name):
            raise NaoCadastradoError(f"Politica({name})", self.path.__str__())

        with self.path.open('w', encoding='utf-8') as file:
            politicas.pop(name)

            json.dump(politicas, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator:bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
