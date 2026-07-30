# Nota de pesquisa — V58

## Pergunta

A barreira bijuntiva da V57 sobrevive quando permitimos reorientar uma ou poucas fibras?

## Resposta obtida

Não para o gadget conhecido: sua profundidade é exatamente um.

Mais geralmente, a pergunta correta é geométrica. Reorientar um alvo significa caminhar no cubo de saídas. Um contexto consistente com bloco redundante é um ponto da imagem na fronteira interna.

Isso produz uma hierarquia:

```text
profundidade 0: orientação inicial suficiente
profundidade 1: flips individuais
profundidade d: busca FPT m^{O(d)}
```

## Resultado experimental exato

Não existe contraexemplo ao flip único entre os circuitos normalizados `0x07`, stretch um, com até oito entradas.

## Questão central restante

A profundidade é limitada por constante para toda a órbita `0x07`?

Uma resposta positiva daria um algoritmo polinomial stretch-one para essa classe. Uma família com profundidade crescente seria uma nova barreira estrutural e orientaria a busca para parâmetros de grafo ou técnicas não locais.
