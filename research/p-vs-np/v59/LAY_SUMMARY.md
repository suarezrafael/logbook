# Resumo para o público leigo — V59

Imagine um aparelho com mais padrões possíveis de luzes do que configurações de botões. Muitos padrões de luzes são impossíveis.

A V58 estudava a distância entre um padrão produzido pelo aparelho e a borda dos padrões possíveis.

A V59 descobriu que essa borda nunca é pequena: mesmo no pior caso, uma parcela da ordem de `1/sqrt(m)` dos padrões produzidos está na borda. Isso vem de um teorema clássico sobre a geometria do cubo de bits.

Mas existe uma diferença importante entre saber que a borda é grande e saber como encontrá-la.

Se aceitarmos sorteio, o problema fica simples: podemos sortear padrões e testar se são possíveis. Como o aparelho tem mais luzes que botões, pelo menos metade dos padrões é impossível.

O desafio científico é encontrar um padrão impossível de maneira determinística.

Tentamos guiar uma caminhada usando três sinais:

- quantos botões já estão obrigatoriamente fixados;
- quantos são fixados por regras locais;
- quantas configurações ainda produzem o padrão.

Uma família adversarial mostrou que os três sinais podem ficar completamente empatados, mesmo quando qualquer passo já chega à borda.

Portanto, a próxima versão precisa de uma regra capaz de atravessar platôs, não apenas de seguir uma subida.

A V59 também começou uma busca computacional mais rigorosa para o caso de nove entradas. A busca tradicional não terminou. Foi preparado um plano usando SAT Modulo Symmetries, uma técnica que evita gerar várias vezes objetos iguais apenas com nomes diferentes.
