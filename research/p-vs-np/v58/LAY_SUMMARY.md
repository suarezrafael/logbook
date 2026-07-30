# Resumo para o público leigo — V58

Imagine um aparelho com mais luzes de saída do que botões de entrada. Queremos encontrar um padrão de luzes que o aparelho nunca consegue produzir.

Nas versões anteriores, escolhíamos para cada luz um estado preferido. O problema é que essa primeira escolha podia formar um sistema perfeitamente possível e sem nenhuma luz obviamente determinada pelas outras.

A V58 permite mudar algumas dessas escolhas.

## A ideia da fronteira

Pense em todos os padrões que o aparelho realmente produz como pontos de uma grande grade. Dois pontos são vizinhos quando diferem em apenas uma luz.

Um ponto está na fronteira quando:

- ele é produzido pelo aparelho;
- mas algum vizinho, obtido trocando uma única luz, não é produzido.

Ao encontrar esse ponto, encontramos imediatamente um padrão impossível.

## O que significa “um flip”

Começamos com um padrão de referência. Um flip significa inverter a preferência de uma única luz antes de analisar as implicações.

A V58 provou que um flip falha somente numa situação muito específica: o aparelho precisa produzir todos os padrões que estão a até duas trocas do padrão inicial.

Isso permite testar a conjectura sem adivinhar qual implicação procurar.

## O que aconteceu com a barreira da V57

A V57 encontrou 12 sistemas pequenos em que nenhuma luz era determinada na escolha inicial.

A V58 descobriu que:

- os 12 são apenas versões renomeadas do mesmo aparelho;
- trocar a orientação de qualquer uma das cinco luzes quebra a barreira;
- depois da troca, três ou quatro luzes ficam determinadas pelas demais;
- o mesmo ocorre na família infinita construída pela V57.

Portanto, a V57 encontrou uma barreira real, mas muito estreita: ela bloqueia somente uma escolha fixa, não uma busca adaptativa.

## Até onde foi a verificação

Um programa exato examinou todas as estruturas normalizadas possíveis para três até oito entradas.

Nenhum circuito exigiu mais de um flip.

Isso não prova que um flip sempre basta para qualquer tamanho. O caso com nove entradas ainda não foi concluído.

## Por que isso é útil

Se o número necessário de flips for pequeno, podemos:

1. testar todas as poucas orientações próximas;
2. usar um algoritmo rápido de 2-SAT em cada uma;
3. encontrar uma saída impossível sem enumerar toda a imagem.

A V58 transforma, assim, uma observação experimental numa medida matemática concreta: **a distância até a fronteira**.
