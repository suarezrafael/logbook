# Teoremas da V59

## Definição 1 — fronteira interna

Para `S ⊆ {0,1}^m`, defina

```text
∂in S = { y in S : existe i com y xor e_i fora de S }.
```

Um ponto `y` pertence à fronteira interna exatamente quando algum flip de uma coordenada produz uma palavra ausente.

## Teorema 1 — abundância isoperimétrica

Se `0 < |S| ≤ 2^(m-1)`, então

```text
|∂in S| ≥ kappa_m |S|,
```

onde

```text
kappa_m = binom(m,floor(m/2)) / 2^(m-1)
        = Theta(1/sqrt(m)).
```

Este é um corolário da solução de Harper para o problema vertex-isoperimétrico do hipercubo. O limite é apertado, até a constante exata, em segmentos simpliciais de meia dimensão.

## Teorema 2 — amostragem por entradas

Seja `C:{0,1}^n->{0,1}^m`, `S=Range(C)` e

```text
alpha = |S| / 2^n.
```

Suponha `|S| ≤ 2^(m-1)`. Para `x` uniforme em `{0,1}^n`:

```text
Pr[C(x) in ∂in S] ≥ kappa_m alpha.
```

### Prova

Cada ponto da imagem possui pelo menos uma preimagem. Portanto,

```text
Pr[C(x) in ∂in S]
  = sum_{y in ∂in S} |C^-1(y)| / 2^n
 >= |∂in S| / 2^n
 >= kappa_m |S| / 2^n
  = kappa_m alpha.
```

## Corolário 2.1 — algoritmo sob promessa de ocupação

Se a pertinência `y in Range(C)` pode ser decidida em tempo polinomial e `alpha ≥ 1/poly(n+m)`, uma saída ausente pode ser encontrada aleatoriamente em tempo polinomial:

1. amostre uma entrada uniforme `x`;
2. calcule `y=C(x)`;
3. teste os `m` vizinhos `y xor e_i`;
4. pare quando um deles estiver fora da imagem.

O número esperado de amostras é

```text
O(sqrt(m)/alpha).
```

Para fibras bijuntivas, cada teste de pertinência é uma instância de 2-SAT.

## Teorema 3 — barreira aos potenciais locais naturais

Na família stretch-one de soma direta da V57, para todo `k ≥ 0`:

```text
n = 4 + 3k,
m = n + 1.
```

A imagem possui um único ponto interior, `1^m`. Todos os seus `m` vizinhos pertencem à fronteira. Entretanto, no ponto interior e em todos os vizinhos:

- a fibra possui exatamente uma preimagem;
- todas as `n` variáveis de entrada estão logicamente forçadas;
- a propagação unitária a partir da descrição 2-CNF força zero variáveis.

Consequentemente, nenhuma regra que exija melhora estrita de qualquer um desses três potenciais consegue justificar o primeiro passo, embora qualquer passo já alcance a fronteira.

## Teorema 4 — limite conceitual da isoperimetria

A abundância de fronteira não fornece, sozinha, um algoritmo determinístico de localização a partir de um baseline fixo. O Teorema 1 controla a quantidade global de pontos de fronteira; ele não identifica uma coordenada de descida nem exclui platôs de potenciais locais.

## Observação randomizada

Para `m>n`, uma palavra uniforme de `{0,1}^m` está fora da imagem com probabilidade pelo menos `1-2^(n-m) ≥ 1/2`. Portanto, quando a pertinência à imagem está em P, o algoritmo Las Vegas mais simples é amostrar diretamente uma palavra de saída. A contribuição isoperimétrica é relevante para localização a partir de pontos conhecidos da imagem e para a análise geométrica, não para superar esse algoritmo randomizado elementar.
