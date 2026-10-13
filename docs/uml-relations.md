# 📄Modelagem das relações entre as classes
Aqui estão descritas os relacionamentos observados entre as classes do sistema (exceto para herança).

Atributos e métodos não foram representados para evitar poluição visual e excesso de detalhes.

- [Click para voltar ao uml](./uml.md)
- [Click para voltar ao readme](../README.md#-classes-planejadas)

### Sumário:
* [Animais](#animais);
* [Lista de Espera](#lista-de-espera);
* [Registros](#registros);
* [Relatórios](#relatórios);

<br>

---

### Animais:
```mermaid
classDiagram
    class Animal {}
    class VacinavelMixin {}
    class Quarentena {}
    class Evento {}
    class Vacina {}

    Animal "1" *-- "0..*" Quarentena : contem (composição)
    Animal "1" *-- "0..*" Evento : contem (composição)
    VacinavelMixin "1" *-- "0..*" Vacina : contem (composição)

```

<br>

---

### Lista de Espera:
```mermaid
classDiagram
    class Animal {}
    class FilaEspera {}
    class EntradaFila {}

    FilaEspera "1" *-- "1..*" EntradaFila : contem (composição)
    FilaEspera "1" o-- "1" Animal : contem (agregação)
    EntradaFila "1" o-- "1" Adotante : contem (agregação)

```

<br>

---

### Registros
```mermaid
classDiagram
    %% Classes que possuem relações
    class Animal {}
    class Adotante {}
    class Adocao {}
    class Devolucao {}
    class Reserva {}

    %% Composições
    Adocao "1" *-- "1" Animal : contem (composição)
    Adocao "1" *-- "1" Adotante : contem (composição)
    Devolucao "1" *-- "1" Animal : contem (composição)
    Devolucao "1" *-- "1" Adotante : contem (composição)
    Reserva "1" *-- "1" Animal : contem (composição)
    Reserva "1" *-- "1" Adotante : contem (composição)

```

---

<br/>

### Relatórios
```mermaid
classDiagram
    %% Classes que possuem relações
    class Animal {}
    class Adotante {}
    class Adocao {}
    class Devolucao {}
    class Top5MaisAdotaveis {}
    class TaxaAdocaoEspecies {}
    class TaxaAdocaoPorte {}
    class TaxaTempoMedioEntradaAdocao {}
    class TaxaDevolucoes {}

    Top5MaisAdotaveis "0..*" o-- "0..*" Animal : possui (agregação)
    Top5MaisAdotaveis "0..*" o-- "0..*" Adotante : possui (agregação)
    
    TaxaAdocaoEspecies "0..*" o-- "0..*" Adocao : possui (agregação)
    TaxaAdocaoPorte "0..*" o-- "0..*" Adocao : possui (agregação)
    
    TaxaTempoMedioEntradaAdocao "0..*" o-- "0..*" Adocao : possui (agregação)
    
    TaxaDevolucoes "0..*" o-- "0..*" Devolucao : possui (agregação)

```

<br>
