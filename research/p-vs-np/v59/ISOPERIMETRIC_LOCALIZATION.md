# Localização isoperimétrica da fronteira

## O que Harper fornece

A fronteira interna nunca é rara quando a imagem ocupa no máximo metade do cubo:

```text
fração mínima = Theta(1/sqrt(m)).
```

Esse resultado transforma a pergunta da V58:

```text
"a fronteira existe perto do baseline canônico?"
```

em duas perguntas mais precisas:

```text
1. Como amostrar uma distribuição que dê peso suficiente à fronteira?
2. Como localizar deterministicamente uma direção quando o baseline é interior?
```

## Três distribuições diferentes

### Palavra uniforme do cubo

Com `m>n`, pelo menos metade das palavras está ausente. Para fibras bijuntivas, basta amostrar uma palavra e testar por 2-SAT. Esperança inferior a duas tentativas.

### Ponto uniforme da imagem

Harper garante probabilidade `Theta(1/sqrt(m))` de cair na fronteira. Entretanto, amostrar uniformemente os pontos distintos da imagem não é imediato.

### Entrada uniforme

A distribuição é ponderada pelo tamanho das fibras. A V59 obtém o limite

```text
Pr[fronteira] ≥ kappa_m alpha,
alpha=|Range(C)|/2^n.
```

## Conclusão metodológica

A isoperimetria resolve a abundância. O problema científico remanescente é um problema de **localização determinística** ou de **amostragem quase uniforme da imagem**, não um problema de existência da fronteira.
