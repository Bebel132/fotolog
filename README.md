# Fotolog AVL

Projeto desenvolvido para a disciplina de Estrutura de Dados utilizando uma Árvore AVL como índice principal para armazenamento e recuperação de fotografias.



## Como executar

```bash

py repl.py

```



ou



```bash

python repl.py

```



### Executar os testes



```bash

py -m unittest tests.py -v

```



ou



```bash

python -m unittest tests.py -v

```



---



## Comandos disponíveis


| Comando                     | Descrição                                            |
| --------------------------- | ---------------------------------------------------- |
| `:add <ts> <path> [rating]` | Adiciona uma foto                                    |
| `:import <manifest.json>`   | Importa fotos de um manifesto JSON                   |
| `:range <ts1> <ts2>`        | Lista fotos entre dois timestamps                    |
| `:nearest <ts>`             | Busca a foto com timestamp mais próximo              |
| `:next <id>`                | Obtém o sucessor da foto                             |
| `:prev <id>`                | Obtém o predecessor da foto                          |
| `:get <id>`                 | Busca foto pelo ID                                   |
| `:tag <id> <tag>`           | Adiciona uma tag                                     |
| `:rate <id> <1..5>`         | Atualiza a avaliação                                 |
| `:find-tag <tag>`           | Busca fotos por tag                                  |
| `:remove <id>`              | Remove uma foto                                      |
| `:remove-range <ts1> <ts2>` | Remove fotos em um intervalo                         |
| `:stats`                    | Exibe estatísticas do catálogo                       |
| `:list`                     | Lista todas as fotos em ordem crescente de timestamp |
| `:tree`                     | Exibe a árvore AVL                                   |
| `:save <arquivo>`           | Salva catálogo em JSON                               |
| `:load <arquivo>`           | Carrega catálogo de JSON                             |
| `:help`                     | Exibe ajuda                                          |
| `:quit`                     | Encerra o programa                                   |

---



## Decisões de Projeto



### Árvore AVL como índice principal



A AVL foi escolhida para garantir:



* Inserção: O(log n)

* Remoção: O(log n)

* Busca: O(log n)



Além disso, permite percorrer os registros em ordem cronológica através do percurso in-order.



### Índice secundário por ID



Como a árvore é ordenada por timestamp, buscas por ID exigiriam percorrer toda a estrutura.



Para evitar isso, foi utilizado um dicionário:



```python

sec_index[id] -> Photo

```



permitindo acesso em tempo O(1).



### Busca por intervalo (range)



A operação foi implementada utilizando poda de subárvores.



Subárvores inteiras são ignoradas quando seus timestamps não podem pertencer ao intervalo consultado.



### Busca nearest



A busca pelo timestamp mais próximo é realizada descendo apenas por um caminho da AVL, mantendo o melhor candidato encontrado até o momento.



Complexidade:



```text

O(log n)

```



### Persistência



Os dados são armazenados em arquivos JSON.



Cada foto é serializada contendo todos os seus atributos.



---



## Formato do JSON



Exemplo:



```json

[

  {

    "id": 1,

    "ts": 1000,

    "path": "foto1.jpg",

    "tags": ["praia"],

    "rating": 5

  }

]

```



---



## Limitações Conhecidas



### IDs não são preservados durante load



Ao carregar um arquivo salvo, novos IDs podem ser gerados para evitar colisões com registros já existentes no catálogo.



Consequência:



* O conteúdo das fotos é preservado.

* Os IDs podem mudar após o carregamento.



### Busca por tags



A busca por tags utiliza o índice secundário e percorre todas as fotos cadastradas.



Complexidade:



```text

O(n)

```



Uma estrutura adicional poderia ser utilizada para indexação por tags.



### Timestamps repetidos



A árvore permite múltiplas fotos com o mesmo timestamp.



A ordenação final depende das regras de inserção da AVL.



### Interface textual



O sistema utiliza uma interface REPL simples baseada em terminal, sem validação avançada de entrada e sem interface gráfica.



---



## Complexidades Principais



| Operação            | Complexidade |
| ------------------- | ------------ |
| Inserção            | O(log n)     |
| Remoção             | O(log n)     |
| Busca por timestamp | O(log n)     |
| Busca por ID        | O(1)         |
| Range               | O(log n + k) |
| Nearest             | O(log n)     |
| Listagem ordenada   | O(n)         |
| Busca por tag       | O(n)         |



onde:



* n = quantidade total de fotos

* k = quantidade de fotos retornadas pela consulta
