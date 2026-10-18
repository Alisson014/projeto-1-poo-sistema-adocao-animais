import json
from pathlib import Path

from ..domain import Adocao, Devolucao, Adotante, Top5MaisAdotaveis, TaxaAdocaoEspecies, TaxaAdocaoPorte, TaxaTempoMedioEntradaAdocao, TaxaDevolucoes
from ..domain import Cachorro, Calopsita, Coelho, Gato
from ..domain.exceptions import NaoCadastradoError


class RelatorioRepository:
    """Classe abstrata para reutilização de código das classes de Relatorio
    
    Attributes:
        path (Path): representa o caminho do arquivo json
    """
    def __init__(self, path):
        self.path = Path(path)

    def get_data(self):
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}

    def generate_id(self) -> int:
        relatorios = self.get_data()

        if not relatorios:
            return 1
        return max(int(id) for id in relatorios.keys())+1

    def delete_all(self, validator:bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)


class Top5MaisAdotaveisRepository(RelatorioRepository):
    """Classe para manipulação de arquivos json referentes ao domínio de Relatório Top5MaisAdotaveis
    
    A classe consegue manipular cada um dos bancos de relatório, sendo que
    as subclasses devem obrigatoriamente ter os métodos from_dict e to_dict

    Attributes:
        path (Path): representa o caminho do arquivo json
    """

    def __init__(self, path):
        super().__init__(path)

    def create(self, relatorio:Top5MaisAdotaveis):
        relatorio.gerar()
        relatorios = self.get_data()

        if relatorios.get(str(relatorio.id)):
            raise Exception(f"{relatorio.id} já cadastrado")

        animais = {
            "Cachorro": [],
            "Calopsita": [],
            "Coelho": [],
            "Gato": []
        }
        for a in relatorio.animais:
            animais[type(a).__name__].append(a.to_dict())

        relatorios[str(relatorio.id)] = relatorio.exportar()

        relatorios[str(relatorio.id)]["animais"] = animais

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

        return True

    def get_all(self):
        relatorios = self.get_data()

        if not relatorios:
            return []

        res = []

        for i in relatorios.keys():
            # utiliza get_by_id para fazer o tratamento dos dados e a instânciação
            res.append(self.get_by_id(i))

        return res

    def get_by_id(self, id):
        relatorios = self.get_data()

        if not relatorios:
            return NaoCadastradoError(f"Top5MaisAdotaveis({id})", self.path.__str__()) 

        if not relatorios.get(str(id)):
            raise NaoCadastradoError(f"Top5MaisAdotaveis({id})", self.path.__str__()) 

        relatorio = relatorios[str(id)]

        animais = []
        for akey in relatorio["animais"].keys():
            match akey:
                case "Cachorro":
                    for animal in relatorio["animais"]["Cachorro"]:
                        animais.append(Cachorro.from_dict(animal))
                case "Calopsita":
                    for animal in relatorio["animais"]["Calopsita"]:
                        animais.append(Calopsita.from_dict(animal))
                case "Coelho":
                    for animal in relatorio["animais"]["Coelho"]:
                        animais.append(Coelho.from_dict(animal))
                case "Gato":
                    for animal in relatorio["animais"]["Gato"]:
                        animais.append(Gato.from_dict(animal))
        relatorio["animais"] = animais

        adotantes = []
        for adot in relatorio["adotantes"]:
            adotantes.append(Adotante.from_dict(adot))

        relatorio["adotantes"] = adotantes

        top5 = []
        # Utiliza os atributos únicos para identificar a subclasse
        for anim in relatorio["top5"]:
            if anim.get("passeios_necessarios_dia") != None:
                top5.append(Cachorro.from_dict(anim))
            elif anim.get("canta") != None:
                top5.append(Calopsita.from_dict(anim))
            elif anim.get("tamanho_gaiola_m3") != None:
                top5.append(Coelho.from_dict(anim))
            elif anim.get("independencia") != None:
                top5.append(Gato.from_dict(anim))

        relatorio["top5"] = top5        

        return Top5MaisAdotaveis.from_dict(relatorio)

    def update(self, new_relatorio:Top5MaisAdotaveis):
        new_relatorio.gerar()
        relatorios = self.get_data()

        if not relatorios.get(str(new_relatorio.id)):
            raise NaoCadastradoError(f"Top5MaisAdotaveis({new_relatorio.id})", self.path.__str__())


        animais = {
            "Cachorro": [],
            "Calopsita": [],
            "Coelho": [],
            "Gato": []
        }
        for a in new_relatorio.animais:
            animais[type(a).__name__].append(a.to_dict())

        relatorios[str(new_relatorio.id)] = new_relatorio.exportar()
        
        relatorios[str(new_relatorio.id)]["animais"] = animais

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

    def delete_by_id(self, id):
        relatorios = self.get_data()

        if not relatorios.get(str(id)):
            raise NaoCadastradoError(f"Top5MaisAdotaveis({id})", self.path.__str__())

        relatorios.pop(str(id))

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

    def delete_all(self, validator:bool):
        # Previne invocações acidentais
        if not validator:
            raise Exception("Operação não confirmada")

        with self.path.open('w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)

class TaxaAdocaoRepository(RelatorioRepository):
    """Classe para manipulação de arquivos json referentes ao domínio de Relatório TaxaAdocao
    
    A classe consegue manipular cada um dos bancos de relatório, sendo que
    as subclasses consideradas são TaxaAdocaoPorte | TaxaAdocaoEspecies | TaxaTempoMedioEntradaAdocao

    Attributes:
        path (Path): representa o caminho do arquivo json
        class_name: Subclasse do registro considerado
    """

    def __init__(self, path, class_name):
        super().__init__(path)
        self.class_name: TaxaAdocaoPorte | TaxaAdocaoEspecies | TaxaTempoMedioEntradaAdocao = class_name

    def create(self, relatorio: TaxaAdocaoEspecies | TaxaAdocaoPorte):
        relatorio.gerar()
        relatorios = self.get_data()

        if relatorios.get(str(relatorio.id)):
            raise Exception("Elemento já cadastrado no banco de dados")

        relatorios[str(relatorio.id)] = relatorio.exportar()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

        return True

    def get_all(self):
        relatorios = self.get_data()

        if not relatorios:
            return []

        res = []
        for i in relatorios.keys():
            res.append(self.get_by_id(i))

        return res

    def get_by_id(self, id):
        relatorios = self.get_data()

        if not relatorios.get(str(id)):
            raise NaoCadastradoError(f"TaxaAdocao({id})", self.path.__str__())

        relatorio = relatorios[str(id)]

        adocoes = []
        for a in relatorio["adocoes"]:
            if a["animal"].get("passeios_necessarios_dia") != None:
                a["animal"] = Cachorro.from_dict(a["animal"])
            elif a["animal"].get("canta") != None:
                a["animal"] = Calopsita.from_dict(a["animal"])
            elif a["animal"].get("tamanho_gaiola_m3") != None:
                a["animal"] = Coelho.from_dict(a["animal"])
            elif a["animal"].get("independencia") != None:
                a["animal"] = Gato.from_dict(a["animal"])

            a["adotante"] = Adotante.from_dict(a["adotante"])

            adocoes.append(Adocao.from_dict(a))

        relatorio["adocoes"] = adocoes

        return self.class_name.from_dict(relatorio)

    def update(self, new_relatorio: TaxaAdocaoPorte | TaxaAdocaoEspecies):
        new_relatorio.gerar()
        relatorios = self.get_data()

        if not relatorios.get(str(new_relatorio.id)):
            raise NaoCadastradoError(f"TaxaAdocao({new_relatorio.id})", self.path.__str__())

        relatorios[str(new_relatorio.id)] = new_relatorio.exportar()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

    def delete_by_id(self, id):
        relatorios = self.get_data()

        if not relatorios.get(str(id)):
            raise NaoCadastradoError(f"TaxaAdocao({id})", self.path.__str__())

        relatorios.pop(str(id))

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)


class TaxaDevolucoesRepository(RelatorioRepository):
    """Classe para manipulação de arquivos json referentes ao domínio de Relatório TaxaAdocao
    
    A classe consegue manipular cada um dos bancos de relatório, sendo que
    a subclasse considerada é TaxaDevolucoes

    Attributes:
        path (Path): representa o caminho do arquivo json
    """

    def __init__(self, path):
        super().__init__(path)

    def create(self, relatorio: TaxaDevolucoes):
        relatorio.gerar()
        relatorios = self.get_data()

        if relatorios.get(str(relatorio.id)):
            raise Exception(f"TaxaDevolucoes({relatorio.id}) já cadastrada na base de dados")

        relatorios[str(relatorio.id)] = relatorio.exportar()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

        return True

    def get_all(self):
        relatorios = self.get_data()

        if not relatorios:
            return []

        res = []

        for i in relatorios.keys():
            res.append(self.get_by_id(i))

        return res
    
    def get_by_id(self, id):
        relatorios = self.get_data()

        if not relatorios.get(str(id)):
            raise NaoCadastradoError(f"TaxaDevolucoes({id})", self.path.__str__())

        relatorio = relatorios[str(id)]

        adocoes = []
        for a in relatorio["adocoes"]:
            if a["animal"].get("passeios_necessarios_dia"):
                a["animal"] = Cachorro.from_dict(a["animal"])
            elif a["animal"].get("canta"):
                a["animal"] = Calopsita.from_dict(a["animal"])
            elif a["animal"].get("tamanho_gaiola_m3"):
                a["animal"] = Coelho.from_dict(a["animal"])
            elif a["animal"].get("independencia"):
                a["animal"] = Gato.from_dict(a["animal"])

            a["adotante"] = Adotante.from_dict(a["adotante"])

            adocoes.append(Adocao.from_dict(a))

        relatorio["adocoes"] = adocoes
        
        devolucoes = []
        for d in relatorio["devolucoes"]:
            if d["animal"].get("passeios_necessarios_dia"):
                d["animal"] = Cachorro.from_dict(d["animal"])
            elif d["animal"].get("canta"):
                d["animal"] = Calopsita.from_dict(d["animal"])
            elif d["animal"].get("tamanho_gaiola_m3"):
                d["animal"] = Coelho.from_dict(d["animal"])
            elif d["animal"].get("independencia"):
                d["animal"] = Gato.from_dict(d["animal"])

            d["adotante"] = Adotante.from_dict(d["adotante"])

            devolucoes.append(Devolucao.from_dict(d))

        relatorio["devolucoes"] = devolucoes

        return TaxaDevolucoes.from_dict(relatorio)
        
    def update(self, new_relatorio: TaxaDevolucoes):
        new_relatorio.gerar()
        relatorios = self.get_data()

        if not relatorios.get(str(new_relatorio.id)):
            raise NaoCadastradoError(f"TaxaDevolucao({new_relatorio.id})", self.path.__str__())

        relatorios[str(new_relatorio.id)] = new_relatorio.exportar()

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)

    def delete_by_id(self, id):
        relatorios = self.get_data()

        if not relatorios.get(str(id)):
            raise NaoCadastradoError(f"TaxaDevolucoes({id})", self.path.__str__())

        relatorios.pop(str(id))

        with self.path.open('w', encoding='utf-8') as file:
            json.dump(relatorios, file, ensure_ascii=False, indent=4)
