# Auditoria da caminhada por potencial

## Potenciais testados

1. número exato de variáveis logicamente forçadas na fibra;
2. número de variáveis fixadas por propagação unitária;
3. `-log2` do tamanho exato da fibra.

O terceiro potencial é computacionalmente caro em geral, mas foi incluído como controle idealizado.

## Resultado adversarial

Na família de soma direta da V57, o único ponto interior e todos os seus vizinhos têm:

```text
preimage size = 1
exact forced variables = n
unit-propagated variables = 0
```

Logo, nenhum dos três potenciais cresce estritamente em uma aresta que sai do interior.

## Resultado aleatório

Em 300 circuitos aleatórios da órbita `0x07`, quase todos os pontos já estavam na fronteira. Um circuito com `n=8` exibiu um platô de propagação unitária em torno de um ponto interior. Os potenciais exato-forçado e tamanho da fibra não falharam nas amostras aleatórias, mas falham na família adversarial explícita.

## Interpretação

A proposta de caminhada continua útil, mas precisa de uma regra que aceite platôs. O próximo candidato deve ser testado contra a família direta antes de qualquer promoção.
