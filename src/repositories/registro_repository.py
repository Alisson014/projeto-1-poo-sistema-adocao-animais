# Declaro utilização de IA para refinamento do código
# O motivo da utilização foi um erro de recursão mútua acusado pelos testes unitários do sistema
# IA utilizada: Claude
# Prompt:
"""
Estou enfrentando um problema quanto à execução de testes unitários com o pytest. 
Não estou conseguindo encontrar a raiz dos erros.

O que está acontecendo é que, os testes são executados até um certo ponto e, quando os testes 
do arquivo registro_repository_test.py são executados, a execução dos testes trava, 
como se caísse em um loop infinito.

Isso aconteceu depois que eu implementei a lógica de que os 
registros modificam os estados dos animais.

Sua tarefa é analisar os testes e os arquivos relacionados para descobrir 
a raiz do problema e resolver a questão dos testes.

Em anexo, enviarei o arquivo de testes e os arquivos 
relacionados ao domínio de registro (model, repository e service)
"""

import json
from pathlib import Path
from datetime import datetime

from ..domain import Adocao, Devolucao, Reserva, Adotante
from ..domain.exceptions import NaoCadastradoError, JaCadastradoError, AnimalIndisponível, TransicaoDeEstadoInvalidaError
from .animal_repository import AnimalRepository
from .pessoa_repository import PessoaRespository
from ..config import PesosCompatibilidade
from ..utils import get_compatibilidade


class RegistroRepository:
    """Classe para manipulação de arquivos json referentes ao domínio de Registro

    Attributes:
        path (Path): representa o caminho do arquivo json
        class_name: Subclasse do registro considerado
    """

    def __init__(self, path, class_name, animal_path, animal_class_name, adotante_path):
        self.path = Path(path)
        self.class_name: type[Adocao | Devolucao | Reserva] = class_name
        self.animal_repository = AnimalRepository(animal_path, animal_class_name)
        self.adotante_repository = PessoaRespository(adotante_path, Adotante)

    # ------------------------------------------------------------------
    # Helpers internos (NENHUM deles chama métodos públicos que limpam o
    # banco, o que evita a recursão mútua get_by_id <-> delete_by_id)
    # ------------------------------------------------------------------

    def __get_data(self) -> dict:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def __save_data(self, registros: dict) -> None:
        with self.path.open('w', encoding='utf-8') as file:
            json.dump(registros, file, ensure_ascii=False, indent=4)

    def __build(self, raw: dict):
        """Monta o objeto de domínio a partir do dict salvo.

        Levanta NaoCadastradoError se o animal ou o adotante não existirem mais.
        Não altera o banco.
        """
        dados = dict(raw)  # cópia: não mexe no dict original
        dados["animal"] = self.animal_repository.get_by_id(dados["animal"])
        dados["adotante"] = self.adotante_repository.get_by_email(dados["adotante"])
        return self.class_name.from_dict(dados)

    @staticmethod
    def __expirada(registro) -> bool:
        # Garante a comparação mesmo com timezones ou padrões diferentes
        if isinstance(registro, Reserva):
            now = datetime.now()
            if registro.data_expiracao.year < now.year:
                return True
            elif registro.data_expiracao.year == now.year:
                if registro.data_expiracao.month < now.month:
                    return True
                elif registro.data_expiracao.month == now.month:
                    if registro.data_expiracao.day < now.day:
                        return True
    
        return False

    def __liberar_animal(self, registro, estrito: bool = True) -> None:
        """Devolve o animal ao estado DISPONIVEL e sincroniza com o banco."""
        try:
            if isinstance(registro, Adocao):
                registro.animal.status = "DEVOLVIDO"
                registro.animal.status = "DISPONIVEL"
            elif isinstance(registro, Reserva):
                # Se o animal da reserva foi adotado, mantém adotado
                if registro.animal.status == "ADOTADO":
                    pass
                elif registro.animal.status == "RESERVADO":
                    registro.animal.status = "DISPONIVEL"

            else:  # Reserva ou Devolucao
                registro.animal.status = "DISPONIVEL"
        except TransicaoDeEstadoInvalidaError:
            if estrito:
                raise AnimalIndisponível(f"{type(registro).__name__} delete")
            return  # limpeza automática: não bloqueia por estado inconsistente

        self.animal_repository.update(registro.animal)

    def __purge(self, id, registro=None) -> None:
        """Remove um registro inválido/expirado do json (limpeza automática)."""
        if registro is not None:
            self.__liberar_animal(registro, estrito=False)

        registros = self.__get_data()
        registros.pop(str(id), None)
        self.__save_data(registros)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def generate_id(self):
        registros = self.__get_data()

        if not registros:
            return 1

        return max(int(id) for id in registros.keys()) + 1

    def create(self, registro: Adocao | Devolucao | Reserva, Pesos: PesosCompatibilidade):
        registros = self.__get_data()

        if registros.get(str(registro.id)):
            raise JaCadastradoError(f"{type(registro).__name__}({registro.id})", self.path.__str__())

        novo_status, nome_erro = {
            Adocao: ("ADOTADO", "Adocao"),
            Reserva: ("RESERVADO", "Reserva"),
            Devolucao: ("DEVOLVIDO", "Devolução"),
        }[type(registro)]

        try:
            registro.animal.status = novo_status
        except TransicaoDeEstadoInvalidaError:
            raise AnimalIndisponível(nome_erro)

        if isinstance(registro, Reserva):
            registro.compatibilidade = get_compatibilidade(registro.animal, registro.adotante, Pesos)

        # Sincroniza com o banco
        self.animal_repository.update(registro.animal)

        registros[str(registro.id)] = registro.to_dict()
        self.__save_data(registros)

        return True

    def get_all(self):
        registros = self.__get_data()

        res = []
        invalidos = []  # (id, registro | None)

        for id, raw in registros.items():
            try:
                registro = self.__build(raw)
            except NaoCadastradoError:
                # Animal/adotante deletado: precaução contra inconsistência
                invalidos.append((id, None))
                continue

            if self.__expirada(registro):
                invalidos.append((id, registro))
                continue

            res.append(registro)

        for id, registro in invalidos:
            self.__purge(id, registro)

        return res

    def get_by_id(self, id):
        registros = self.__get_data()

        raw = registros.get(str(id))
        if not raw:
            raise NaoCadastradoError(f"Registro({id})", self.path.__str__())

        try:
            registro = self.__build(raw)
        except NaoCadastradoError:
            self.__purge(id)
            raise NaoCadastradoError(f"Registro({id})", self.path.__str__())

        if self.__expirada(registro):
            self.__purge(id, registro)
            raise NaoCadastradoError(f"Reserva({id}) expirada", self.path.__str__())

        return registro

    def update(self, new_registro: Adocao | Devolucao | Reserva):
        registros = self.__get_data()

        if not registros.get(str(new_registro.id)):
            raise NaoCadastradoError(f"Registro({new_registro.id})", self.path.__str__())

        # Atualizar um registro NÃO deve mudar o estado do animal:
        # a transição já ocorreu no create.
        registros[str(new_registro.id)] = new_registro.to_dict()
        self.__save_data(registros)

    def delete_by_id(self, id):
        registros = self.__get_data()

        raw = registros.get(str(id))
        if not raw:
            raise NaoCadastradoError(f"Registro({id})", self.path.__str__())

        try:
            registro = self.__build(raw)
        except NaoCadastradoError:
            # Animal/adotante não existe mais: só remove o registro órfão
            self.__purge(id)
            return

        self.__liberar_animal(registro, estrito=True)

        registros.pop(str(id))
        self.__save_data(registros)

    def delete_all(self, validator: bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        registros = self.__get_data()

        for raw in registros.values():
            try:
                registro = self.__build(raw)
            except NaoCadastradoError:
                continue
            self.__liberar_animal(registro, estrito=False)

        self.__save_data({})
