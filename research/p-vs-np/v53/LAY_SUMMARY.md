# Resumo para o público leigo — V53, corrigido pela V54

> **Resultado assintótico retirado.** A alegação de que ciclos longos forçariam grau de síndrome crescente estava errada. Use a V54 como registro científico atual.

## O que permaneceu correto?

Para um circuito formado por portas `AND₃`, cada produto de saídas corresponde à união dos suportes das portas escolhidas.

Se dois grupos pequenos de portas sempre tiverem uniões diferentes, esses produtos continuam algebricamente independentes. Essa transferência `union-free → independência de baixo grau` permanece válida.

Os dois exemplos finitos também permanecem corretos:

- UF2 tem grau exato 3;
- UF3 tem grau exato 4.

## Qual foi o erro?

A V53 afirmava que girth elevado no grafo de incidência impediria todas as colisões de união.

Isso é falso quando um grupo de arestas contém o outro. Uma aresta pode estar completamente coberta pela união de outras três sem criar ciclo algum.

Exemplo:

```text
e  = {0,1,2}
f0 = {0,3,4}
f1 = {1,5,6}
f2 = {2,7,8}
```

O grafo de incidência é uma árvore, mas:

```text
union({f0,f1,f2}) = union({e,f0,f1,f2}).
```

Por isso, foram retirados:

- `girth > 4t ⇒ t-union-free`;
- a família com suposto grau `Ω(log n)`;
- a conclusão de que síndromes de grau constante falhariam nessa família.

## Qual foi o resultado positivo escondido no erro?

A V54 provou o sentido oposto para circuitos puros `AND₃` com mais saídas que entradas.

O hipergrafo possui um 2-core. Dentro dele, uma porta central é forçada por no máximo três portas testemunhas. Isso produz a equação:

```text
(1-Y_e) · Y_f1 · Y_f2 · Y_f3 = 0.
```

Assim, existe sempre uma palavra ausente com separador de grau no máximo quatro.

## O que aprendemos?

A infraestrutura de verificação precisa testar não apenas ciclos curtos, mas também colisões por cobertura e contenção.

O caso realmente aberto continua sendo `NC⁰₃-Avoid` geral, especialmente para portas ternárias fora da órbita de `AND₃` e suas negações.
