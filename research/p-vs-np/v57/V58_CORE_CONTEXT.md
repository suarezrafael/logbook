# Contexto congelado para o Laboratório V58

## Fatos estáveis

1. As retratações da V53 permanecem válidas.
2. V54 resolve `AND_k` stretch positivo por forcing core, com separador de grau `k+1`.
3. V56 resolve toda mistura de fibras afins no stretch mínimo `m>n`.
4. As classes afins essenciais resolvidas são `0x01`, `0x06`, `0x18`, `0x69`.
5. As classes não afins restantes são `0x07`, `0x16`, `0x17`, `0x19`, `0x1b`, `0x1e`.
6. `0x07`, `0x17`, `0x1b` possuem ambas as fibras bijuntivas.
7. Todo conjunto booleano próprio possui uma aresta de fronteira e, portanto, forcing por contexto completo.
8. Esse forcing é apenas existencial e não distingue classes.
9. A consistência-or-redundância direta é falsa para blocos bijuntivos.
10. Há um gadget mínimo `0x07` com `n=4,m=5`, solução comum única e zero blocos redundantes.
11. Há uma família infinita `n=4+3k,m=n+1` com a mesma propriedade.
12. A contagem de SCCs e a quantidade de variáveis forçadas não substituem o posto linear.
13. A literatura já estuda redundância e irredundância em 2-CNF; novidade não confirmada.
14. O rascunho de consulta de prior art foi criado, mas não enviado.
15. Os verificadores autocontidos ausentes da V56 foram publicados na mesma branch.

## Foco obrigatório

Encontrar uma estrutura algorítmica para localizar uma aresta de fronteira em imagens bijuntivas sem enumerar a imagem.

## Rotas prioritárias

1. Dominadores no grafo de implicação.
2. Cortes mínimos e pares de caminhos para forçar uma saída.
3. Núcleos mínimos de implicação por blocos, não por cláusulas individuais.
4. Branching nas duas células afins de cada fibra, com parâmetro estrutural explícito.
5. Algoritmo FPT por número de SCCs não triviais, feedback vertex set ou treewidth do grafo de implicação.
6. Misturas de fibras afins e `0x07`.
7. Procurar contraexemplos para cada medida antes de formular teorema.
8. Revisar respostas dos autores, caso o rascunho seja enviado.

## Critérios de promoção

- algoritmo stretch-one para `0x07`, `0x17` ou `0x1b`;
- algoritmo FPT rigoroso para uma medida do grafo de implicação;
- novo contraexemplo mínimo que derrube uma medida proposta;
- equivalência formal com uma noção conhecida de redundância 2-CNF;
- confirmação ou correção externa de prior art.
