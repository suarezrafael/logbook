# Resumo para o público leigo — V55

A V55 passou de portas com uma única combinação especial para portas em que duas combinações produzem o mesmo valor especial.

A classe central aceita duas combinações opostas, como `011` e `100`. Essas combinações são descritas por duas regras de paridade. Assim, cada saída representa um pequeno bloco de equações lineares.

Quando existem mais portas que variáveis, não há espaço suficiente para todos os blocos serem independentes. Pelo menos uma porta inteira fica determinada pelas demais. Pedimos então que as portas determinantes assumam seus valores especiais e que a porta determinada assuma o valor oposto. Essa palavra de saída é impossível.

A classe é genuinamente ternária, não monotônica e admite algoritmo com apenas uma saída a mais que entradas.

A classificação completa encontrou 14 classes NPN. Quatro classes essenciais têm fibras afins e seis classes essenciais permanecem não afins:

```text
0x07, 0x16, 0x17, 0x19, 0x1b, 0x1e.
```

A V55 resolve uma subclasse nova, mas não resolve `NC0_3-Avoid` geral nem P versus NP.
