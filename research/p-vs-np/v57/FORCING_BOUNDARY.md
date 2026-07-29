# Forcing de contexto completo e fronteira do hipercubo

## Lema

Todo conjunto não vazio e próprio `S subset {0,1}^m` possui um ponto `y in S` e uma coordenada `i` para os quais `y xor e_i` não pertence a `S`.

## Certificado separador

Defina o literal indicador

```text
L_j(Y_j) = Y_j       se y_j=1,
           1-Y_j     se y_j=0.
```

O polinômio

```text
Q(Y) = L_0(Y_0)...L_{i-1}(Y_{i-1}) L_{i+1}(Y_{i+1})...L_{m-1}(Y_{m-1})
       * (1-L_i(Y_i))
```

vale um em `y xor e_i` e zero em toda a imagem: qualquer ponto da imagem que tenha o contexto `y_{-i}` precisa ter o bit `y_i`.

O grau é `m`. No stretch um, `m=n+1`.

## Interpretação correta da evidência aleatória

Encontrar empiricamente uma porta forçada por todas as demais é inevitável em qualquer imagem própria. O fenômeno não distingue classes fáceis de classes difíceis.

A pergunta algorítmica correta é:

> É possível localizar uma aresta de fronteira a partir da descrição local do circuito sem enumerar a imagem?

A V57 não responde positivamente a essa pergunta.
