
# 🧱 Decisões de Design:
Este arquivo apresenta um registro das decisões de design utilizadas ao longo do desenvolvimento deste projeto.

[Click aqui para voltar ao readme](../README.md#-decisões-de-design)

<br>

## 1. Arquitetura inicial:

### Motivo:
A arquitetura inicial utilizada visa atender tanto aos requitos do trabalho, como também manter um alinhamento com padrões de mercado, para assim construir uma base sólida de conhecimento.

### Implicações:
Adicionar uma arquitetura de pastas base contendo apenas arquivos vazios.

---

<br>

## 2. Gitflow e Conventional commits:

### Motivo:
Melhorar a organização do projeto e alinhá-lo aos padrões de mercado. Além de ser uma forma em que eu posso praticar para utilizar esse padrão de maneira cada vez mais natural e consistente.

### Implicações:
Regras e padrões de nomenclatura para branchs e commits, além de definir o fluxo de desenvolvimento utilizado no projeto.

---

<br>

## 3. Padrão Google para docstrings:

### Motivo:
Requisito técnico do projeto e algo com grande valor para o desenvolvimento do projeto, auxiliando a manter uma documentação clara e alinhando o projeto aos padrões de mercado e às boas práticas de programação.

### Implicações:
A estrutura das docstrings das classes do projeto deverá seguir as seguintes regras e forma:
```python
class MinhaClasse:
    """Linha de resumo curta explicando o propósito da classe.

    Uma descrição mais longa e detalhada sobre o funcionamento da classe,
    seu comportamento e como utilizá-la, se necessário.

    Attributes:
        atributo1 (str): Descrição do primeiro atributo público.
        atributo2 (int): Descrição do segundo atributo. Opcionalmente,
            pode ocupar múltiplas linhas com recuo adequado.
    """

    def __init__(self, atributo1: str, atributo2: int):
        """Inicializa a classe com os valores fornecidos."""
        self.atributo1 = atributo1
        self.atributo2 = atributo2
```

**Regras Principais:**
* **Delimitadores**: Sempre utilize três aspas duplas (`"""`) no início e no final.
* **Linha de Resumo**: Deve ocupar apenas uma linha, terminar com um ponto final e resumir o objetivo da classe.
* **Linha em Branco**: Insira uma linha em branco entre o resumo e a descrição detalhada, bem como antes de seções especiais.
* **Seção `Attributes`**: Documenta os atributos públicos da instância logo na docstring da classe (no mesmo formato da seção `Args` de funções). O tipo do atributo é indicado entre parênteses após o nome.
* **Método `__init__`**: Pode ter sua própria docstring caso os parâmetros de inicialização precisem de explicações detalhadas que não constam nos atributos da classe.

---

<br>

## 4. Type hints em todo o código:

### Motivo:
Requisito técnico do projeto e uma ótima maneira de seguir tipagem para boas práticas de programação.

### Implicações:
Utilização de type hints em todo o código e utilização da biblioteca mypy para verificação de código.

---

<br>

## 5. Utilizar requirements.txt e requirements-dev.txt

### Motivo:
Facilitar a instalação das dependêcias utilizadas no projeto.

### Implicações:
Popular os arquivos `requirements.txt` e `requirements-dev.txt` com as dependências utilizadas no projeto.

---

<br>
