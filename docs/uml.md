
# 📄UML Textual
Aqui estão descritas as classes iniciais pensadas para o projeto, juntamente com seus `atribútos`, `métodos principais` e `relacionamentos` (herança);

Esta descrição é apenas um ponto de partida para o desenvolvimento do projeto, não necessariamente se manterá inauterada até o fim do desenvolvimento.

[Click para voltar ao readme](../README.md#-classes-planejadas)

### Sumário:
* [Animais](#animais);
* [Pessoas](#pessoa);
* [Lista de Espera](#lista-de-espera);
* [Registros](#registros);
* [Quarentena](#quarentena);
* [Relatórios](#relatorios);
* [Políticas configuráveis](#politicas-configuráveis);
* [Auxiliares](#classes-auxiliares);

<br>

---

### Animais:
```mermaid
classDiagram
    %% Classes
    class Animal{
        + id: int;
        + especie: string;
        + nome: string;
        + sexo: MACHO, FEMEA;
        + idade_meses: int;
        + data_entrada: Date;
        + porte: P, M, G;
        + status: DISPONIVEL, RESERVADO, ADOTADO, DEVOLVIDO, QUARENTENA, INADOTAVEL;
        + energia: CALMO, HIPERATIVO;
        + historico: List[Evento];
        + temperamento: List[ARISCO, DÓCIL, MEDROSO];
        + cuidado_especial: bool;
        + envelhecer() -> None;
        + adicionar_evento(evento: Evento) -> None;
        + remover_evento(evento: Evento) -> None;
        + atualizar_status() -> None;
        - __valida_transicao_status() -> bool;
        + get_historico() -> List[dict];
    }

    class VacinavelMixin {
        + vacinas: List[Vacina];
        + vacinar() -> None;
        + get_vacinas() -> list[dict]
    }

    class AdestravelMixin {
        + nivel_adestramento: int;
        + adestrar() -> None;
    }

    class Cachorro {
        + raca: string;
        + passeios_necessarios_dia: int;
    }

    class Gato {
        + raca: string;
        + independencia: bool;
    }
    
    class Coelho {
        + raca: string;
        + tamanho_gaiola_m3: float;
    }

    class Calopsita {
        + canta: bool;
        + ensinar_a_cantar() -> None;
    }

    %% Relacionamentos
    Animal <|-- Cachorro : Herança (é um)
    VacinavelMixin <|-- Cachorro : Herança (mixin)
    AdestravelMixin <|-- Cachorro : Herança (mixin)
    
    Animal <|-- Gato : Herança (é um)
    VacinavelMixin <|-- Gato : Herança (mixin)
    AdestravelMixin <|-- Gato : Herança (mixin)
    
    Animal <|-- Coelho : Herança (é um)
    VacinavelMixin <|-- Coelho : Herança (mixin)
    AdestravelMixin <|-- Coelho : Herança (mixin)
    
    Animal <|-- Calopsita : Herança (é um)
    AdestravelMixin <|-- Calopsita : Herança (mixin)
```

<br>
<br>

---

### Pessoa:
```mermaid
classDiagram
    %% Classes:
    class Pessoa {
        + nome: string;
        - email: string;
        + idade: int;
    }

    class Adotante {
        + moradia: APARTAMENTO_COM_VARANDA, APARTAMENTO_SEM_VARANDA, CASA_COM_QUINTAL, CASA_SEM_QUINTAL;
        + experiencia: INICIANTE, INTERMEDIÁRIO, AVANÇADO;
        + tempo_livre_min: int;
        + possui_criancas: bool;
        + outros_animais: bool;
        + area_util: float;
    }

    %% Relacionamentos:
    Pessoa <|-- Adotante : Herança (é um)
```

<br>
<br>

---

### Lista de Espera:
```mermaid
classDiagram
    %% Classes
    class EntradaFila {
        + adotante: dict;
        + tempo_espera: int;
        + compatibilidade: float;
    }

    class FilaEspera {
        + animal: int;
        + fila: List[EntradaFila];
        + add(adotante: Adotante) -> None;
        + remove(adotante: Adotante) -> None;
        + proximo() -> EntradaFila;
        + get_fila() -> list[dict];
    }
```    

<br>
<br>

---


### Registros:
```mermaid
classDiagram
    class Registro {
        + id: int;
        + animal: Animal;
        + adotante: Adotante;
    }

    class Reserva {
        + data_inicial: datetime;
        + data_expiracao: datetime;
        + status: ATIVA, CANCELADA, EXPIRADA;
        + compatibilidade: float;
    }

    class Adocao {
        + taxa: float;
        + pago: bool;
        + data: datetime;
        + calcular_taxa() -> None;
        + gerar_contrato() -> str;
        + registrar_pagamento() -> None;
    }

    class Devolucao {
        + motivo: COMPORTAMENTO, PESSOAL, DOENCA, OUTRO;
        + data: datetime;
    }

    %% Relacionamentos:
    Registro <|-- Reserva : Herança (é um)
    Registro <|-- Adocao : Herança (é um)
    Registro <|-- Devolucao : Herança (é um)
```

<br>
<br>

---

### Quarentena:
```mermaid
classDiagram
    class Quarentena {
        + animal: int;
        + data_inicial: datetime;
        + data_final: null | datetime;
        + motivo: COMPORTAMENTO, DOENCA, OUTRO;
        + status: ATIVA, CUMPRIDA;
    }
```

<br>
<br>

---

### Relatorios:
```mermaid
classDiagram
    class Relatorio {
        + id: int;
        + data: datetime;
        + nome: string
        + gerar();
        + exportar();
    }

    class Top5MaisAdotaveis {
        + animais: List[Animal];
        + adotantes: List[Adotante];
        + top5: List[dict];
    }

    class TaxaAdocaoEspecies {
        + adocoes: List[Adocao];
        + taxas: dict;
    }

    class TaxaAdocaoPorte {
        + adocoes: List[Adocao];
        + taxas: dict;
    }

    class TaxaTempoMedioEntradaAdocao {
        + adocoes: List[Adocao];
        + tempo_medio_meses: int;
    }

    class TaxaDevolucoes {
        + adocoes: List[Adocao];
        + devolucoes: List[Devolucao];
        + taxa: string
    }

    %% Relacionamentos
    Relatorio <|-- Top5MaisAdotaveis : Herança (é um)
    Relatorio <|-- TaxaAdocaoEspecies : Herança (é um)
    Relatorio <|-- TaxaAdocaoPorte : Herança (é um)
    Relatorio <|-- TaxaTempoMedioEntradaAdocao : Herança (é um)
    Relatorio <|-- TaxaDevolucoes : Herança (é um)
```

<br>
<br>

---

### Politicas configuráveis:
```mermaid
classDiagram
    %% Classes:
    class Politica {
        + nome: string;
        + data_modificacao: datetime;
        + validar() -> bool;
    }

    class IdadeMinima {
        + idade_minima: int;
        + validar(idade) -> bool;
    }

    class PorteXArea {
        + porte_p_min: float;
        + porte_m_min: float;
        + porte_g_min: float;
        + validar(porte, area) -> bool;
    }

    class DuracaoReserva {
        + duracao_dias: int;
    }

    class PesosCompatibilidade {
        + peso_porte_moradia: float;
        + peso_experiencia_temperamento: float;
        + peso_tempo_livre_energia: float;
        + peso_criancas_temperamento: float;
    }

    %% Relacionamentos:
    Politica <|-- IdadeMinima : Herança (é um)
    Politica <|-- PorteXArea : Herança (é um)
    Politica <|-- DuracaoReserva : Herança (é um)
    Politica <|-- PesosCompatibilidade : Herança (é um)
```

<br>
<br>

---

### Classes auxiliares:
```mermaid
classDiagram
    class Evento {
        + tipo: VACINA, ADOCAO, DEVOLUCAO, QUARENTENA, CONSULTA;
        + descricao: string;
        + data: datetime;
    }

    class Vacina {
        + nome: string;
        + data: datetime;
    }
```
