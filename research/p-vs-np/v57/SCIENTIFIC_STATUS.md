# Estado científico da V57

## Demonstrado internamente

- todo subconjunto booleano próprio não vazio possui um contexto completo que força um bit;
- o gadget `n=4,m=5` da órbita `0x07` é consistente e completamente irredundante;
- o gadget possui solução única e quatro SCCs;
- existe uma família infinita stretch-one de blocos `0x07` consistentes e irredundantes;
- a analogia direta de consistência-ou-redundância da V56 é falsa para fibras bijuntivas;
- a contagem simples de SCCs e a quantidade de variáveis forçadas não substituem o posto linear.

## Confirmado por computação exaustiva

- `n=3,m=4`: 249.900 multisets da órbita, nenhum contraexemplo consistente irredundante;
- `n=4,m=5`, normalizado pela solução comum zero: 376.992 famílias, exatamente 12 completamente irredundantes;
- 65.804 subconjuntos próprios de cubos de dimensão até quatro possuem aresta de fronteira.

## Conhecido ou próximo da literatura

- 2-CNF e relações bijuntivas são clássicas;
- redundância e subconjuntos irredundantes de 2-CNF já foram estudados;
- ciclos e SCCs são estruturas centrais no estudo de 2-SAT;
- `NC0_3-Avoid` geral no stretch mínimo permanece aberto.

## Não confirmado

- prioridade do gadget `0x07` em contexto de Range Avoidance;
- prioridade da família assintótica de blocos orientados;
- melhor vocabulário para a noção de redundância por blocos de fibras;
- existência de algoritmo eficiente para `0x07-Avoid` stretch-one.

## Não demonstrado

- algoritmo stretch-one para qualquer uma das seis classes não afins;
- impossibilidade de toda medida de potencial em grafos de implicação;
- dureza de `0x07-Avoid`;
- lower bound de circuitos;
- separação P versus NP.

## Decisão

A V57 é promovida como **teorema de barreira/correção de rota**, não como avanço algorítmico positivo.
