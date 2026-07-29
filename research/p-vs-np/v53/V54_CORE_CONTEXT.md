# Contexto central para o Laboratório V54

## Fatos estáveis da V53

1. O alvo principal agora é stretch-one `NC⁰₃-Avoid`; `NC⁰₄` fica como controle de barreira.
2. Para um hipergrafo 3-uniforme `H`, o circuito `AND₃` associa a cada edge uma saída monomial.
3. Se `H` é t-union-free, a substituição dos monômios de saída de grau até `t` é injetiva sobre qualquer corpo.
4. Portanto, `sd_F(Range(C_H)) > t`.
5. Incidence girth maior que `4t` implica t-union-free.
6. Há famílias randomized-constructible de stretch um com `sd_F = Omega(log n)`.
7. A família é monotônica; monotone `NC⁰₃-Avoid` já é polinomial. O resultado é barreira ao método de síndromes, não dureza de Avoid.
8. Exemplo UF2: `(n,m)=(8,9)`, grau exato 3 sobre GF(2).
9. Exemplo UF3: `(n,m)=(15,16)`, grau exato 4 sobre GF(2).
10. As matrizes de avaliação até o limiar são full-rank sobre GF(2), GF(3) e GF(5).
11. Output flips preservam o grau, mas isso não transforma a prova numa família ternária arbitrária.
12. Prioridade bibliográfica da transferência union-free→syndrome permanece não confirmada.

## Foco principal da V54

**Encontrar uma ferramenta construtiva para NC⁰₃-Avoid que sobreviva quando não existem síndromes globais de grau constante.**

## Prioridades

1. Estudar `sepdeg(S,y)` e procurar alvos fáceis mesmo quando `sd(S)` é alto.
2. Combinar o algoritmo Turán para a subclasse monotônica com certificados algébricos locais.
3. Testar portas ternárias não monotônicas e NPN classes essenciais.
4. Procurar famílias não monotônicas de grau crescente sem confundir isso com dureza.
5. Relacionar equal-union collisions a hypergraph containers e ao trabalho de Cameron Seth sobre estruturas tolerantes.
6. Procurar uma construção determinística explícita de incidência high-girth com constantes quantitativas.
7. Investigar síndromes esparsas, circuit-size da síndrome e Ideal Proof System, não apenas grau.
8. Preparar contato com GGNS perguntando sobre prior art, Hilbert functions e union-free terminology; não enviar sem decisão explícita.

## Critérios de promoção

- algoritmo novo para uma subclasse ternária não coberta;
- teorema sobre separating degree que produza alvos em tempo polinomial;
- extensão não monotônica rigorosa da barreira de grau;
- prior art confirmado ou correção por especialistas;
- conexão formal que converta Turán/containers/hitting sets em um algoritmo de Avoid.
