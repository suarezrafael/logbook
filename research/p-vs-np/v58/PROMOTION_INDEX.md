# Índice de promoção — V58

O índice abaixo é uma regra interna de decisão, não uma avaliação de revista ou probabilidade de correção.

| Critério congelado | Pontos | Justificativa |
|---|---:|---|
| Enunciado matemático falsificável | 2/2 | profundidade, bola de Hamming e algoritmo definidos exatamente |
| Prova ou censo exato | 2/2 | teoremas gerais provados; censo completo até `n=8` |
| Consequência algorítmica | 1/2 | algoritmo FPT por profundidade, mas não algoritmo geral para `0x07` |
| Supera ou esclarece a V57 | 1/1 | barreira reclassificada como profundidade um |
| Dois verificadores independentes | 1/1 | Python independente e busca C++ exata |
| Reprodutibilidade no repositório | 1/1 | código, resultados, logs e manifesto incluídos |
| Resultado assintótico novo sobre a classe | 0/1 | apenas a família V57 tem profundidade um provada |
| Prioridade externa confirmada | 0/1 | contato não enviado; literatura próxima existe |
| Impacto direto em `NC0_3-Avoid` geral | 0/1 | fronteira geral permanece aberta |
| Impacto direto em P versus NP | 0/1 | nenhum |

## Pontuação

\[
\boxed{8/12}
\]

## Decisão

```text
PROMOVIDO COMO RESULTADO ESTRUTURAL/FPT PARCIAL
NÃO PROMOVIDO COMO ALGORITMO GERAL PARA 0x07
```

A promoção se deve à equivalência geométrica, ao algoritmo parametrizado, à auditoria completa do gadget e ao censo exato até `n=8`.
