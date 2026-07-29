# Teoremas da V57

## Definição — redundância de um bloco orientado

Sejam `F_1,...,F_m` subconjuntos de `{0,1}^n`, representando fibras ativas escolhidas para as saídas. O bloco `F_i` é redundante quando

```text
intersection_{j != i} F_j subseteq F_i.
```

Nesse caso, ativar os demais blocos força o bloco `i` a ficar ativo.

## Teorema 1 — forcing universal de borda

Para todo conjunto não vazio e próprio

```text
S proper subset of {0,1}^m,
```

existem `y in S` e uma coordenada `i` tais que

```text
y xor e_i notin S.
```

Equivalentemente, dentro de `S`, fixar todas as coordenadas diferentes de `i` nos valores `y_{-i}` força a coordenada `i` a valer `y_i`.

### Consequência para Range Avoidance

Toda imagem de um circuito com `m>n` possui um certificado existencial de forcing usando todas as outras `m-1` saídas.

Esse teorema não fornece um algoritmo eficiente para localizar a fronteira.

## Teorema 2 — contraexemplo mínimo à redundância bijuntiva direta

Existe um circuito com `n=4`, `m=5`, cujas cinco portas pertencem à órbita NPN de `0x07`, e uma orientação para a fibra de três pontos de cada porta, tal que:

1. todas as cinco fibras são bijuntivas;
2. a interseção das cinco fibras é `{0000}`;
3. nenhum bloco é redundante em relação aos outros quatro.

Um exemplo é dado pelos blocos:

```text
B1 = ¬x0 ∧ (¬x1 ∨  x2)
B2 = ¬x0 ∧ ( x1 ∨ ¬x2)
B3 = ¬x0 ∧ (¬x1 ∨  x3)
B4 = ¬x0 ∧ ( x1 ∨ ¬x3)
B5 = ¬x0 ∧ (¬x2 ∨ ¬x3).
```

O exemplo é mínimo sob a convenção de portas ternárias essenciais com três entradas distintas: para `n=3,m=4`, uma busca exaustiva sobre os `249.900` multisets da órbita `0x07` mostrou que toda orientação pelas fibras pequenas é inconsistente ou possui um bloco redundante.

A minimalidade é computacional finita; o contraexemplo `n=4,m=5` e sua irredundância possuem prova direta.

## Teorema 3 — família stretch-one completamente irredundante

Para todo inteiro `k>=0`, existe um circuito da órbita `0x07` com

```text
n=4+3k,
m=5+3k=n+1,
```

tal que as fibras pequenas orientadas são conjuntamente consistentes e nenhum bloco é redundante.

A família é a soma direta do gadget `n=4,m=5` com `k` cópias de um gadget balanceado `n=m=3` formado pelas máscaras `0x07,0x0b,0x0d`.

## Corolário — não existe análogo direto do posto afim

A proposição

```text
m>n and consistent bijunctive blocks
    => some complete gate block is implied by the others
```

é falsa, mesmo numa única órbita NPN ternária e no stretch mínimo.

No gadget explícito, o grafo de implicação possui quatro componentes fortemente conexas e `m=5`, mas nenhum bloco é redundante. Portanto, a simples contagem de SCCs também não pode substituir o posto da V56.

## Escopo

Os teoremas não excluem:

- algoritmos que escolham orientações de forma adaptativa;
- branching entre células afins;
- certificados de inconsistência;
- medidas mais sofisticadas do grafo de implicação;
- algoritmos específicos para `0x07`, `0x17` ou `0x1b`.
