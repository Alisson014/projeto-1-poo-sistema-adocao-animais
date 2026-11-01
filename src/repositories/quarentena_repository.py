import json
from pathlib import Path

from ..domain.models import Quarentena
from ..domain.exceptions import NaoCadastradoError, JaCadastradoError, TransicaoDeEstadoInvalidaError, AnimalIndisponível
from .animal_repository import AnimalRepository


class QuarentenaRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de Quarentena

    A classe consegue manipular cada um dos bancos de quarentena, sendo que
    a classe deve obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
        animal_repository: AnimalRepository do tipo de animal considerado
    """

    def __init__(self, path, class_name, animal_path):
        self.path = Path(path)
        self.animal_repository: AnimalRepository = AnimalRepository(animal_path, class_name)

    # ------------------------------------------------------------------
    # Helpers internos (nenhum chama métodos públicos que limpam o banco)
    # ------------------------------------------------------------------

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def __save_data(self, quarentenas: dict) -> None:
        with self.path.open('w', encoding='utf-8') as file:
            json.dump(quarentenas, file, ensure_ascii=False, indent=4)

    def __build(self, raw: dict) -> Quarentena:
        """Monta o objeto de domínio a partir do dict salvo.

        Levanta NaoCadastradoError se o animal não existir mais.
        Não altera o banco.
        """
        dados = dict(raw)  # cópia: não mexe no dict original
        dados["animal"] = self.animal_repository.get_by_id(dados["animal"])
        return Quarentena.from_dict(dados)

    def __liberar_animal(self, quarentena: Quarentena, estrito: bool = True) -> None:
        """Devolve o animal ao estado DISPONIVEL e sincroniza com o banco.

        Só faz algo se a quarentena ainda está ATIVA: uma quarentena já
        cumprida não é dona do estado atual do animal.
        """
        if quarentena.status != "ATIVA":
            return

        try:
            quarentena.animal.status = "DISPONIVEL"
        except TransicaoDeEstadoInvalidaError:
            if estrito:
                raise AnimalIndisponível("Quarentena delete")
            return  # limpeza em lote: não bloqueia por estado inconsistente

        self.animal_repository.update(quarentena.animal)

    def __purge(self, id) -> None:
        """Remove uma quarentena órfã (animal inexistente) do json."""
        quarentenas = self.__get_data()
        quarentenas.pop(str(id), None)
        self.__save_data(quarentenas)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def generate_id(self) -> int:
        quarentenas = self.__get_data()

        # O primeiro id é sempre 1
        if not quarentenas:
            return 1

        # retorna o incremento do último id
        return max(int(id) for id in quarentenas.keys()) + 1

    def create(self, quarentena: Quarentena):
        quarentenas = self.__get_data()

        if str(quarentena.id) in quarentenas:
            raise JaCadastradoError(f"Quarentena({quarentena.id})", self.path.__str__())

        # Um animal não pode cumprir duas quarentenas ao mesmo tempo.
        # (sem `break`: qualquer quarentena ATIVA do animal bloqueia)
        for raw in quarentenas.values():
            if raw["animal"] == quarentena.animal.id and raw["status"] == "ATIVA":
                raise JaCadastradoError(
                    f"Quarentena ativa do animal({quarentena.animal.id})", self.path.__str__()
                )

        try:
            quarentena.animal.status = "QUARENTENA"
        except TransicaoDeEstadoInvalidaError:
            raise AnimalIndisponível("Quarentena")

        # Sincroniza com o banco de dados
        self.animal_repository.update(quarentena.animal)

        quarentenas[str(quarentena.id)] = quarentena.to_dict()
        self.__save_data(quarentenas)
        return True

    def get_all(self):
        quarentenas = self.__get_data()

        res = []
        invalidos = []

        for id, raw in quarentenas.items():
            try:
                res.append(self.__build(raw))
            except NaoCadastradoError:
                # Animal deletado: precaução contra falhas de consistência
                invalidos.append(id)

        for id in invalidos:
            self.__purge(id)

        return res

    def get_by_id(self, id: int):
        quarentenas = self.__get_data()

        raw = quarentenas.get(str(id))
        if not raw:
            raise NaoCadastradoError(f"Quarentena({id})", self.path.__str__())

        try:
            return self.__build(raw)
        except NaoCadastradoError:
            # Limpa a quarentena inválida do banco
            self.__purge(id)
            raise NaoCadastradoError(f"Quarentena({id})", self.path.__str__())

    def update(self, new_quarentena: Quarentena):
        quarentenas = self.__get_data()

        antigo = quarentenas.get(str(new_quarentena.id))
        if not antigo:
            raise NaoCadastradoError(f"Quarentena({new_quarentena.id})", self.path.__str__())

        # O estado do animal só muda quando o status da quarentena muda
        # (reaplicar o mesmo estado causaria transição inválida).
        if antigo["status"] != new_quarentena.status and new_quarentena.status == "CUMPRIDA":
            try:
                new_quarentena.animal.status = "DISPONIVEL"
            except TransicaoDeEstadoInvalidaError:
                raise AnimalIndisponível("Quarentena")

            # Sincroniza com o banco de dados
            self.animal_repository.update(new_quarentena.animal)

        quarentenas[str(new_quarentena.id)] = new_quarentena.to_dict()
        self.__save_data(quarentenas)

    def delete_by_id(self, id: int):
        quarentenas = self.__get_data()

        raw = quarentenas.get(str(id))
        if not raw:
            raise NaoCadastradoError(f"Quarentena({id})", self.path.__str__())

        try:
            quarentena = self.__build(raw)
        except NaoCadastradoError:
            # Animal não existe mais: só remove o registro órfão
            self.__purge(id)
            return

        self.__liberar_animal(quarentena, estrito=True)

        quarentenas.pop(str(id))
        self.__save_data(quarentenas)

    def delete_all(self, validator: bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        quarentenas = self.__get_data()

        for raw in quarentenas.values():
            try:
                quarentena = self.__build(raw)
            except NaoCadastradoError:
                continue
            self.__liberar_animal(quarentena, estrito=False)

        self.__save_data({})
