# Profundidade de orientação

## Definição operacional

A profundidade `rho` mede quantos valores de saída precisam ser reorientados antes de encontrarmos um contexto consistente que force alguma coordenada.

Ela é a distância da orientação inicial até a fronteira interna da imagem.

## Interpretação algorítmica

| Profundidade | Significado | Custo de busca |
|---:|---|---:|
| 0 | a orientação inicial é ausente ou já força uma saída | polinomial |
| 1 | basta testar a orientação inicial e cada flip único | `O(m^2 poly(n+m))` |
| 2 | testar flips simples e duplos | `O(m^3 poly(n+m))` |
| d constante | FPT por enumeração de orientações | `m^{O(d)} poly(n+m)` |
| sem limite | não fornece algoritmo polinomial geral | potencialmente exponencial |

## Diferença para a V57

A V57 mostrou que a orientação fixa pode ser consistente e irredundante. A V58 mostra que isso não significa distância grande até a fronteira.

No gadget mínimo e em sua família por soma direta:

```text
redundância na orientação inicial: não
profundidade de orientação: 1
```

## Critério geométrico

A profundidade excede `d` exatamente quando a imagem contém uma bola de Hamming de raio `d+1` ao redor do ponto inicial.

Isso permite usar:

- algoritmos 2-SAT para procurar a fronteira;
- argumentos de cardinalidade para limites universais;
- censos exatos por capacidade das fibras;
- ferramentas isoperimétricas para versões futuras.
