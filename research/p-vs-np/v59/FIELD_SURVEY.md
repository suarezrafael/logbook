# Pesquisa de campo — V59

## Harper e isoperimetria do hipercubo

Harper resolveu o problema vertex-isoperimétrico do cubo Booleano: segmentos iniciais da ordem simplicial minimizam a vizinhança para cardinalidade fixa. Trabalhos modernos de estabilidade reiteram essa formulação e caracterizam conjuntos próximos dos extremizadores.

Aplicação na V59: para conjuntos de tamanho no máximo metade do cubo, a fração mínima de fronteira interna é `Theta(1/sqrt(m))`.

Referências:

- Harper's vertex-isoperimetric theorem, conforme resumido em Przykucki–Roberts, *Vertex-isoperimetric stability in the hypercube*, JCTA 2020, DOI `10.1016/j.jcta.2019.105186`.
- Raty, *Uniqueness in Harper's vertex-isoperimetric theorem*, arXiv:1806.11061.

## SAT Modulo Symmetries

Kirchweger e Szeider integram um solver CDCL a um propagador de minimalidade lexicográfica que testa objetos parcialmente definidos e aprende cláusulas para eliminar ramos não canônicos.

Referências:

- Kirchweger–Szeider, *SAT Modulo Symmetries for Graph Generation*, CP 2021, DOI `10.4230/LIPIcs.CP.2021.34`.
- Kirchweger–Szeider, *SAT Modulo Symmetries for Graph Generation and Enumeration*, ACM TOCL 2024, DOI `10.1145/3670405`.

## Provas verificáveis

A extensão de SMS para matroides incorporou geração de provas DRAT para validar axiomas adicionais produzidos pela verificação de minimalidade.

- Kirchweger–Scheucher–Szeider, *A SAT Attack on Rota's Basis Conjecture*, SAT 2022, DOI `10.4230/LIPIcs.SAT.2022.4`.

## Limite da caminhada

A literatura de random walks no hipercubo estuda hitting times de conjuntos grandes, mas abundância de fronteira não fornece automaticamente um caminho determinístico a partir de um ponto adversarial. A V59 não promove um bound de hitting time.

## Prioridade bibliográfica

A formulação específica

```text
image boundary + 2-SAT membership + input-occupancy parameter
```

não foi localizada como teorema nomeado. Ela é uma combinação elementar de ferramentas conhecidas; novidade não é reivindicada.
