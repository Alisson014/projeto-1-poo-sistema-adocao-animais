# Declaro utilização de IA para geração do código abaixo
# IA utilizada: claude
# Tomei essa decisão em decorrência do pouco tempo que possuo para finalizar a entrega 4
# prompt:
"""
##### Mensagem 1

Estou desenvolvendo um sistema de gerenciamento de adoção de animais em python, 
como avaliação da disciplina de Poo da minha graduação em engenharia de software. 
Esse sistema está organizado em uma hierarquia de modularização que segue models, 
repositories, services e, por fim, api (com FastAPI).

No momento, estou desenvolvendo os services dos domínios desse sistema. 
Para desenvolvê-los, estou adotando um processo de validação via testes 
unitários codificados em pytest.

A partir desse contexto, sua tarefa é criar a classe de service do domínio 
que lhe enviarei e os testes unitários referentes à ela, mantendo o mesmo padrão de 
código que venho utilizando nesse projeto (Lhe enviarei arquivos de exemplo em anexo, 
ambos são referentes ao domínio de animal).

O service que você codificará, juntamente com seus testes, será o domínio de relatório.
Para lhe auxiliar, estou enviando o arquivos com os repositories de relatório 
(cada subclasse de RelatorioRepository deve ter seu próprio service)

##### Mensagem 2
##### As primeiras versões foram codificadas a partir de deduções do agente a respeito 
##### Dos models utilizados, por isso a necessidade da segunda mensagem

Antes de realizar essas implementações no sistema, lhe auxiliarei a ter mais segurança 
na codificação desses módulo lhe informando os models utilizados:
Cada um estará disponível em anexo.

Também realizei as alterações sugeridas nos repositories de relatório.

Dessa forma, gere a versão finas dos services e de seus testes.
"""


from ..domain import Top5MaisAdotaveis
from ..repositories import Top5MaisAdotaveisRepository
from ..domain import TaxaAdocaoPorte, TaxaAdocaoEspecies, TaxaTempoMedioEntradaAdocao
from ..repositories import TaxaAdocaoRepository, PoliticaRepository
from ..domain import TaxaDevolucoes
from ..repositories import TaxaDevolucoesRepository



class Top5MaisAdotaveisService:
    """Classe para modelar os serviços referentes ao domínio de relatório Top5MaisAdotaveis

    A classe é responsável por garantir o cumprimento das regras de negócio
    e a utilização do repository

    Attributes:
        repository (Top5MaisAdotaveisRepository): Repository do relatório Top5MaisAdotaveis
        politica_repository (PoliticaRepository): Repository de Política para buscas os pesos de compatibilidade
    """

    def __init__(self, path: str, path_politica:str):
        self.repository = Top5MaisAdotaveisRepository(path)
        self.politica_repository = PoliticaRepository(path_politica)

    def create(self, relatorio_data: dict):
        # O top5 é sempre calculado por gerar(), então nunca é recebido de fora.
        # Passá-lo explicitamente evita o uso da lista padrão mutável do model
        # relatorio_data = {**relatorio_data, "top5": []}

        # Instancia classe model
        # As exceções de validação são lançadas pela classe model
        relatorio = Top5MaisAdotaveis(**relatorio_data, id=self.repository.generate_id())
        relatorio.pesos_compatibilidade = self.politica_repository.get_by_name("PesosCompatibilidade")

        # O método gerar() é invocado dentro do repository
        self.repository.create(relatorio)

        return relatorio

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def update(self, relatorio_data: dict, relatorio_id: int):
        updated_relatorio: Top5MaisAdotaveis = self.repository.get_by_id(int(relatorio_id))

        # Atualiza apenas os atributos informados
        # Como há validação na classe, as exceptions serão disparadas pela classe.
        for key, value in relatorio_data.items():
            if hasattr(updated_relatorio, key) and key != "id":
                setattr(updated_relatorio, key, value)

        updated_relatorio.pesos_compatibilidade = self.politica_repository.get_by_name("PesosCompatibilidade")

        # gerar() acrescenta animais ao top5, então o top5 anterior é descartado
        # para que o relatório seja recalculado do zero
        updated_relatorio.top5 = []

        # O método gerar() é invocado dentro do repository
        self.repository.update(updated_relatorio)
        return updated_relatorio

    def delete_by_id(self, id: int | str):
        self.repository.delete_by_id(id)

    def delete_all(self):
        self.repository.delete_all(True)



class TaxaAdocaoService:
    """Classe para modelar os serviços referentes ao domínio de relatório TaxaAdocao

    A classe é responsável por garantir o cumprimento das regras de negócio
    e a utilização do repository. Cada instância trabalha com uma única subclasse
    de relatório (TaxaAdocaoPorte | TaxaAdocaoEspecies | TaxaTempoMedioEntradaAdocao)

    Attributes:
        model (type): Subclasse de relatório considerada
        repository (TaxaAdocaoRepository): Repository do relatório considerado
    """

    def __init__(self, path: str, class_name: type[TaxaAdocaoPorte] | type[TaxaAdocaoEspecies] | type[TaxaTempoMedioEntradaAdocao]):
        self.model = class_name
        self.repository = TaxaAdocaoRepository(path, class_name)

    def create(self, relatorio_data: dict):
        # Instancia classe model
        # As exceções de validação são lançadas pela classe model
        relatorio = self.model(**relatorio_data, id=self.repository.generate_id())

        # O método gerar() é invocado dentro do repository
        self.repository.create(relatorio)

        return relatorio

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def update(self, relatorio_data: dict, relatorio_id: int):
        updated_relatorio = self.repository.get_by_id(int(relatorio_id))

        # Atualiza apenas os atributos informados
        # Como há validação na classe, as exceptions serão disparadas pela classe.
        for key, value in relatorio_data.items():
            if hasattr(updated_relatorio, key) and key != "id":
                setattr(updated_relatorio, key, value)

        # O método gerar() é invocado dentro do repository
        self.repository.update(updated_relatorio)
        return updated_relatorio

    def delete_by_id(self, id: int | str):
        self.repository.delete_by_id(id)

    def delete_all(self):
        self.repository.delete_all(True)




class TaxaDevolucoesService:
    """Classe para modelar os serviços referentes ao domínio de relatório TaxaDevolucoes

    A classe é responsável por garantir o cumprimento das regras de negócio
    e a utilização do repository

    Attributes:
        repository (TaxaDevolucoesRepository): Repository do relatório TaxaDevolucoes
    """

    def __init__(self, path: str):
        self.repository = TaxaDevolucoesRepository(path)

    def create(self, relatorio_data: dict):
        # Instancia classe model
        # As exceções de validação são lançadas pela classe model
        relatorio = TaxaDevolucoes(**relatorio_data, id=self.repository.generate_id())

        # O método gerar() é invocado dentro do repository
        self.repository.create(relatorio)

        return relatorio

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def update(self, relatorio_data: dict, relatorio_id: int):
        updated_relatorio: TaxaDevolucoes = self.repository.get_by_id(int(relatorio_id))

        # Atualiza apenas os atributos informados
        # Como há validação na classe, as exceptions serão disparadas pela classe.
        for key, value in relatorio_data.items():
            if hasattr(updated_relatorio, key) and key != "id":
                setattr(updated_relatorio, key, value)

        # O método gerar() é invocado dentro do repository
        self.repository.update(updated_relatorio)
        return updated_relatorio

    def delete_by_id(self, id: int | str):
        self.repository.delete_by_id(id)

    def delete_all(self):
        self.repository.delete_all(True)
