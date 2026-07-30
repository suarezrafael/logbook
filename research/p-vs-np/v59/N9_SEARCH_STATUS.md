# Estado da busca exata n=9

## Busca DFS herdada da V58

Executada com 8 threads e limite de 100.000 nós por ramo superior.

| Tipo canônico | Nós visitados | Contraexemplo | Completa |
|---:|---:|---:|---:|
| 1 | 3.559.977 | não | não |
| 3 | 2.637.185 | não | não |

Os arquivos brutos são:

- `N9_SEARCH_PARTIAL.csv`;
- `N9_SEARCH_PARTIAL_TYPE3.csv`.

## Interpretação correta

A ausência de contraexemplos nessa busca parcial não é evidência matemática suficiente para promover a conjectura do flip único.

## Próximo mecanismo

Substituir a enumeração DFS por SAT Modulo Symmetries, usando geração canônica dinâmica e, idealmente, prova DRAT verificável.
