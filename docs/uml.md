
# 📄UML Textual
Aqui estão descritas as classes iniciais pensadas para o projeto, juntamente com seus `atribútos`, `métodos principais` e `relacionamentos` (herança);

Esta descrição é apenas um ponto de partida para o desenvolvimento do projeto, não necessariamente se manterá inauterada até o fim do desenvolvimento.

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
        + adicionar_evento() -> None;
        + atualizar_status() -> None;
        + _validar_transicao_status() -> bool;
        + get_historico() -> string;
    }

    class VacinavelMixin {
        + vacinas: List[Vacina];
        + vacinar() -> None;
    }

    class AdestravelMixin {
        + adestrado: bool;
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
        + tamanho_gaiola_cm2: float;
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
        + get_email() -> string;
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
        + adotante: (id) Adotante;
        + timestamp_entrada: datetime;
        + compatibilidade: float;
    }

    class FilaEspera {
        + animal: (id) Animal;
        + fila: List[EntradaFila];
        + add() -> None;
        + remove() -> None;
        + proximo() -> Adotante;
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
        + animal: (id) Animal;
        + adotante: (id) Adotante;
    }

    class Reserva {
        + data_inicial: date;
        + data_expiracao: date;
        + status: ATIVA, CANCELADA, EXPIRADA;
        + compatibilidade: float;
        + confirmar();
        + expirar();
        + cancelar();
    }

    class Adocao {
        + taxa: float;
        + pago: bool;
        + data: date;
        + gerar_contrato() -> String;
        + registrar_pagamento() -> void;
    }

    class Devolucao {
        + motivo: COMPORTAMENTO, PESSOAL, DOENCA;
        + data: date;
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
        + animal: (id) Animal;
        + data_inicial: date;
        + data_final: null | date;
        + motivo: COMPORTAMENTO, DOENCA;
        + status: ATIVA, CUMPRIDA;
        + atualizar_status(novo_status: Enum) -> None;
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
        + data: date;
        + nome: string;
        + gerar() -> None;
        + exportar() -> string;
    }

    class Top5MaisAdotaveis {
        + animais: List[Animal];
        + Adotantes: List[Adotante];
        + top5: List[Animal];
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
        + animais: List[Animal];
        + adocoes: List[Adocao];
        + tempo_medio_dias: int;
    }

    class TaxaDevolucoes {
        + data_inicial: date;
        + data_final: date;
        + devolucoes: List[Devolucao];
    }

    %% Relacionamentos
    Relatorio <|-- Top5MaisAdotaveis : Herança (é um)
    Relatorio <|-- TaxaAdocaoEspecies : Herança (é um)
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
        + data_modificacao: date;
        + validar(**kwars) -> bool; 
    }

    class IdadeMinima {
        idade_minima: int;
    }

    class PorteXArea {
        + porte_p_min: float;
        + porte_m_min: float;
        + porte_g_min: float;
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
        tipo: VACINA, ADOCAO, DEVOLUCAO, QUARENTENA, CONSULTA;
        descricao: string;
        data: date;
    }

    class Vacina {
        nome: string;
        data: date;
    }

```
