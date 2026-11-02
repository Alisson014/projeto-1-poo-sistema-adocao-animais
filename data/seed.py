from src.api.paths import AnimalPath, FilaEsperaPath, PessoaPath, QuarentenaPath, RegistroPath, RelatorioPath, PoliticaPath
from pathlib import Path
import json

# ======================
# Paths dos arquivos de persistência
# ======================

animal_path = AnimalPath()
fila_espera_path = FilaEsperaPath()
pessoa_path = PessoaPath()
quarentena_path = QuarentenaPath()
registro_path = RegistroPath()
relatorio_path = RelatorioPath()
politica_path = PoliticaPath()


# ======================
# Persistindo animais
# ======================
from .data_seed import cachorro, calopsita, coelho, gato

INSERT_ANIMAL_MAP = {
    animal_path.cachorro: cachorro,
    animal_path.calopsita: calopsita,
    animal_path.coelho: coelho,
    animal_path.gato: gato
}

for path, data in INSERT_ANIMAL_MAP.items():
    with Path(path).open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ======================
# Persistindo politicas
# ======================
from .data_seed import politicas

with Path(politica_path.path).open('w', encoding='utf-8') as file:
    json.dump(politicas, file, ensure_ascii=False, indent=4)


# ======================
# Persistindo pessoas
# ======================
from .data_seed import adotante

with Path(pessoa_path.adotante).open('w', encoding='utf-8') as file:
    json.dump(adotante, file, ensure_ascii=False, indent=4)


# ======================
# Persistindo quarentenas
# ======================
from .data_seed import q_cachorro

with Path(quarentena_path.cachorro).open('w', encoding='utf-8') as file:
    json.dump(q_cachorro, file, ensure_ascii=False, indent=4)


# ======================
# Persistindo registros
# ======================
from .data_seed import a_cachorro, d_cachorro, r_cachorro

INSERT_REGISTRO_MAP = {
    registro_path.a_cachorro: a_cachorro,
    registro_path.d_cachorro: d_cachorro,
    registro_path.r_cachorro: r_cachorro
}

for path, data in INSERT_REGISTRO_MAP.items():
    with Path(path).open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ======================
# Persistindo relatorios
# ======================
from .data_seed import top5, adocao_especies, adocao_porte, tempo_medio_entrada_adocao, taxa_devolucoes

INSERT_RELATORIO_MAP = {
    relatorio_path.top5_mais_adotaveis: top5,
    relatorio_path.taxa_adocao_especies: adocao_especies,
    relatorio_path.taxa_adocao_porte: adocao_porte,
    relatorio_path.taxa_tempo_medio_entrada_adocao: tempo_medio_entrada_adocao,
    relatorio_path.taxa_devolucoes: taxa_devolucoes
}

for path, data in INSERT_RELATORIO_MAP.items():
    with Path(path).open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ======================
# Persistindo filas de espera
# ======================
from .data_seed import fila_cachorro, fila_calopsita, fila_coelho, fila_gato

INSERT_FILA_ESPERA_MAP = {
    fila_espera_path.fila_cachorro_path: fila_cachorro,
    fila_espera_path.fila_calopsita_path: fila_calopsita,
    fila_espera_path.fila_coelho_path: fila_coelho,
    fila_espera_path.fila_gato_path: fila_gato
}

for path, data in INSERT_FILA_ESPERA_MAP.items():
    with Path(path).open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


print("\n Dados carregados com sucesso \n")
