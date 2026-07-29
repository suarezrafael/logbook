# Contexto histórico da V54 — substituído pelo resultado final da V54

> **Este arquivo registrava o plano da V54 antes da descoberta do contraexemplo. Não deve ser usado como contexto científico atual.**

## Fatos preservados da V53

1. O alvo principal continua sendo stretch-one `NC⁰₃-Avoid`.
2. Para um hipergrafo 3-uniforme `H`, o circuito puro `AND₃` associa uma saída monomial a cada aresta.
3. Se `H` é `t`-union-free, a substituição dos monômios de saída de grau até `t` é injetiva sobre qualquer corpo.
4. Portanto, `sd_F(Range(C_H)) > t`.
5. UF2 tem grau exato 3.
6. UF3 tem grau exato 4.

## Fatos retirados

As seguintes afirmações deste contexto preliminar eram falsas:

```text
incidence girth > 4t => t-union-free;
stretch-one AND3 com sd_F = Ω(log n).
```

O argumento ignorava colisões aninhadas, nas quais uma aresta está coberta pela união de outras arestas. Essas colisões podem ocorrer em grafos de incidência acíclicos.

## Resultado final da V54

A V54 provou:

1. todo hipergrafo `k`-uniforme com `|E|>|V|` possui um 2-core não vazio;
2. uma aresta do core é coberta por no máximo `k` arestas testemunhas;
3. para circuito puro `AND_k`, isso produz:

```text
(1-Y_e) product_f Y_f = 0;
```

4. existe um alvo ausente com `sepdeg <= k+1`;
5. para `AND₃`, o limite é quatro;
6. a construção estende-se à órbita ternária singleton-fiber por literais assinados em regimes especificados.

## Contexto atual

Use:

```text
research/p-vs-np/v54/V55_CORE_CONTEXT.md
```

como contexto congelado para o próximo laboratório.
