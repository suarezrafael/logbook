# Resumo para o público leigo — V57

## O que tentávamos fazer

Na versão anterior, as condições das portas eram equações de paridade. Quando havia mais portas que botões, a álgebra linear garantia que alguma condição era repetida ou consequência das outras.

Na V57 tentamos aplicar a mesma ideia a condições do tipo:

> Se esta coisa acontecer, então aquela outra precisa acontecer.

Essas condições são representadas por fórmulas 2-CNF e grafos de implicação.

## O que a experiência aleatória parecia mostrar

Em milhares de circuitos aleatórios, sempre aparecia uma luz cujo valor era determinado pelas outras luzes.

A V57 descobriu que essa observação, sozinha, não é especial: qualquer conjunto incompleto de padrões de luz possui uma borda. Em algum padrão possível, trocar uma única luz produz um padrão impossível.

O problema é encontrar essa borda sem listar todos os padrões.

## O contraexemplo

Construímos cinco portas usando apenas quatro botões.

Todas as cinco condições podem ser satisfeitas ao mesmo tempo, mas nenhuma é desnecessária. Quando retiramos qualquer uma delas, aparece uma configuração que satisfaz as outras quatro e viola exatamente a retirada.

Portanto, a regra simples:

> “Há mais portas que botões, então alguma condição precisa ser repetida”

funciona para equações lineares, mas não funciona para implicações lógicas.

## Por que isso é útil

O resultado evita que a próxima versão invista numa analogia falsa.

Ele também mostra que contar componentes do grafo ou contar quantos botões ficaram determinados não basta. Precisamos de uma ferramenta que use mais informação sobre os caminhos e ciclos das implicações.

## O que não foi resolvido

Ainda não encontramos um algoritmo geral para essas portas. A V57 apenas prova que o caminho mais direto da V56 não pode funcionar.

A próxima versão vai procurar uma medida mais refinada, como dominadores, cortes, pares de caminhos ou núcleos mínimos de implicação.
