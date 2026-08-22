# 🧠 Grafo de Conhecimento — Sistema de Treinos

Projeto desenvolvido para representar e manipular uma **Base de Conhecimento utilizando Grafos**, relacionando alunos, objetivos, exercícios, músculos trabalhados e máquinas utilizadas nos exercícios.

O projeto utiliza **Python, Pandas e NetworkX** para armazenar, manipular e visualizar as relações entre os elementos da base de conhecimento.

---

## 📌 Sobre o projeto

O sistema foi desenvolvido com o objetivo de aplicar conceitos de **Estrutura de Dados e Grafos** em um cenário de academia.

As informações são representadas por meio de relações no formato:

```text
Aluno → relação → informação
```

Por exemplo:

```text
Paola → tem objetivo → Emagrecimento
Paola → treina → Agachamento
Agachamento → trabalha → Quadríceps
Agachamento → ativa → Glúteo
Leg 45° → usa máquina → Leg Press
```

Dessa forma, o sistema consegue representar uma pequena **rede de conhecimento sobre treinamentos físicos**.

---

## 🎯 Objetivos

* Aplicar conceitos de **grafos direcionados**;
* Representar uma base de conhecimento utilizando relações entre entidades;
* Permitir a inserção e remoção de nós;
* Permitir a criação e remoção de relacionamentos;
* Consultar informações relacionadas a determinado nó;
* Consultar exercícios que trabalham ou ativam determinado músculo;
* Visualizar graficamente a estrutura da base de conhecimento;
* Integrar um `DataFrame` do Pandas com uma estrutura de grafo;
* Utilizar diferentes camadas para representar alunos, objetivos, exercícios, músculos e máquinas.

---

## 🗂️ Estrutura da Base de Conhecimento

A base de conhecimento é armazenada inicialmente em um `DataFrame` do Pandas com três colunas:

| Head          | Relação      | Tail          |
| ------------- | ------------ | ------------- |
| Paola         | tem objetivo | Emagrecimento |
| Lucas         | tem objetivo | Hipertrofia   |
| Paola         | treina       | Agachamento   |
| Agachamento   | trabalha     | Quadríceps    |
| Agachamento   | ativa        | Glúteo        |
| Tríceps Testa | trabalha     | Tríceps       |
| Leg 45°       | usa máquina  | Leg Press     |

Esse modelo utiliza o conceito de **triplas**, muito utilizado na representação de conhecimento:

```text
(Head, Relação, Tail)
```

Exemplo:

```text
(Agachamento, trabalha, Quadríceps)
```

---

## 🕸️ Estrutura do Grafo

O sistema transforma as relações da base de conhecimento em um **grafo direcionado (`DiGraph`)** utilizando a biblioteca NetworkX.

A estrutura pode ser representada conceitualmente como:

```text
                    ┌───────────────┐
                    │  Emagrecimento│
                    └───────▲───────┘
                            │
                      tem objetivo
                            │
                        ┌───┴───┐
                        │ Paola │
                        └───┬───┘
                            │
                          treina
                            │
                      ┌─────▼─────┐
                      │Agachamento│
                      └─────┬─────┘
                            │
                         trabalha
                            │
                      ┌─────▼─────┐
                      │ Quadríceps│
                      └───────────┘
```

---

## ⚙️ Funcionalidades

O sistema possui um menu interativo no terminal.

### 1. Inserir nó

Permite adicionar um novo nó ao grafo.

```text
Digite o nó que deseja adicionar:
```

---

### 2. Remover nó

Remove um nó e seus relacionamentos associados do grafo e também atualiza a base de conhecimento.

---

### 3. Inserir relacionamento

Permite criar uma nova relação entre dois nós.

Exemplo:

```text
Head: Cleyton
Relação: treina
Tail: Agachamento
```

Resultado:

```text
Cleyton → treina → Agachamento
```

---

### 4. Remover relacionamento

Remove uma relação específica informando:

```text
Head
Relação
Tail
```

---

### 5. Consultar relacionamentos

Permite consultar todas as relações existentes a partir de determinado nó.

Exemplo:

```text
Paola
```

Pode retornar:

```text
[('tem objetivo', 'Emagrecimento'),
 ('treina', 'Agachamento')]
```

---

### 6. Listar nós

Exibe todos os nós existentes no grafo.

---

### 7. Listar relacionamentos

Exibe todas as triplas existentes:

```text
('Paola', 'tem objetivo', 'Emagrecimento')
('Paola', 'treina', 'Agachamento')
('Agachamento', 'trabalha', 'Quadríceps')
```

---

### 8. Visualizar a Base de Conhecimento

Exibe o `DataFrame` utilizado como base de conhecimento.

---

### 9. Visualizar o Grafo

Utiliza o **NetworkX + Matplotlib** para gerar uma representação visual do grafo.

Os elementos são organizados em diferentes categorias:

* 🔵 **Alunos**
* 🟣 **Objetivos**
* 🟠 **Exercícios**
* 🟢 **Músculos**
* ⚫ **Máquinas**

---

### 10. Consultar por músculo

Permite informar um músculo e encontrar os exercícios que o trabalham ou ativam.

Exemplo:

```text
Digite o músculo desejado: Glúteo
```

Resultado:

```text
Agachamento → ativa → Glúteo
Leg 45° → ativa → Glúteo
```

Além da consulta textual, o sistema gera um **grafo filtrado** mostrando apenas os relacionamentos relacionados ao músculo escolhido.

---

## 🛠️ Tecnologias utilizadas

* **Python 3**
* **Pandas** — armazenamento e manipulação da base de conhecimento
* **NetworkX** — criação e manipulação dos grafos
* **Matplotlib** — visualização gráfica


O sistema apresentará o menu:

```text
-------------------- MENU ------------------
1 - Inserir nó
2 - Remover nó
3 - Inserir relacionamento
4 - Remover relacionamento
5 - Consultar relacionamento
6 - Listar nós
7 - Listar Relacionamentos
8 - Ver Base de conhecimento
9 - Mostrar grafo
10 - Consultar grafo por músculo e visualização
11 - Encerrar
```

---

## 🧩 Conceitos de Estrutura de Dados aplicados

O projeto utiliza diversos conceitos estudados em **Estrutura de Dados**, incluindo:

* Grafos direcionados;
* Nós e arestas;
* Listas de adjacência;
* Inserção e remoção de nós;
* Inserção e remoção de arestas;
* Busca e consulta de relacionamentos;
* Representação de dados por triplas;
* Visualização de grafos.

A estrutura principal utilizada para representar o grafo é um **dicionário com listas de adjacência**:

```python
self.grafo = {
    "Paola": [
        ("tem objetivo", "Emagrecimento"),
        ("treina", "Agachamento")
    ]
}
```

---

## 🔍 Exemplo de utilização

Considere a seguinte sequência:

```text
Paola → treina → Agachamento

Agachamento → trabalha → Quadríceps

Agachamento → ativa → Glúteo
```

O sistema consegue responder a consultas como:

> Quais exercícios trabalham o Quadríceps?

Resultado:

```text
Agachamento → trabalha → Quadríceps
Leg 45° → trabalha → Quadríceps
```

Também é possível visualizar essas relações graficamente através do NetworkX.


## 👩‍💻 Autoria

Projeto desenvolvido como atividade acadêmica para aplicação prática dos conceitos de **Estrutura de Dados, Grafos e Representação de Conhecimento**.

**Paola Hanna**

Estudante de Engenharia da Computação — UPE

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e de aprendizado.

