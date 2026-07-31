# Plano SAT Modulo Symmetries para o caso n=9

## Objetivo

Gerar, livre de isomorfismos, um circuito da órbita `0x07` com:

```text
n=9, m=10,
```

cuja orientação canônica de fibra pequena e todos os dez flips simples falhem em produzir inconsistência ou bloco redundante.

## Codificação existencial

A propriedade de contraexemplo pode ser codificada em SAT.

Para cada uma das 11 orientações relevantes:

1. inclua uma atribuição testemunha que satisfaz todos os blocos;
2. para cada bloco `j`, inclua uma atribuição testemunha que satisfaz todos os outros blocos e viola o bloco `j`.

Essas testemunhas certificam simultaneamente:

- consistência;
- irredundância completa.

Não é necessário usar QBF para essa propriedade finita.

## Representação para SMS

Representar o circuito como grafo colorido:

- 9 vértices de variável;
- 10 vértices de porta;
- nós de incidência coloridos para a posição fixada e para o par lateral;
- cor adicional para o tipo proibido `1`, `2` ou `3`.

As simetrias principais são:

```text
S_9 sobre variáveis × S_10 sobre portas,
```

com a troca dos dois terminais laterais acompanhada da troca dos tipos proibidos `1 ↔ 2`.

## Por que SMS é apropriado

SMS combina CDCL com verificação dinâmica de minimalidade lexicográfica em objetos parcialmente definidos. Isso evita a redução estática incompleta que apareceu durante a V58.

O framework já foi estendido para produzir provas DRAT em aplicações a matroides. A V59 não implementou ainda a prova DRAT para esta codificação específica; isso permanece requisito da V60.

## Estado operacional

- codificação matemática: preparada;
- representação por grafo colorido: preparada;
- implementação PySMS: não concluída;
- execução `n=9`: não realizada por SMS;
- certificado DRAT: não gerado.
