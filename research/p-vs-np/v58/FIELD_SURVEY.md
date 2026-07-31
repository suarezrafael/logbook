# Pesquisa de campo — V58

## 1. Range Avoidance de baixa localidade

Gajulapalli, Golovnev, Nagargoje e Saraogi registram que `NC0_2-Avoid` possui algoritmo polinomial, enquanto `NC0_3-Avoid` permanece aberto no stretch mínimo. Eles também conectam algoritmos em stretches maiores à construção de matrizes rígidas e lower bounds para circuitos de profundidade logarítmica.

Referência:

- K. Gajulapalli, A. Golovnev, S. Nagargoje, S. Saraogi, *Range Avoidance for Constant-Depth Circuits: Hardness and Algorithms*, ECCC TR23-021 / APPROX-RANDOM 2023.

## 2. Redundância em 2-CNF

A redundância de cláusulas e os subconjuntos equivalentes irredundantes de fórmulas 2-CNF possuem literatura própria. Liberatore mostra que a estrutura cíclica influencia a complexidade de vários problemas de irredundância.

Referência:

- P. Liberatore, *Redundancy in Logic II: 2CNF and Horn Propositional Formulae*, Artificial Intelligence 172 (2008), 265–299, DOI 10.1016/j.artint.2007.06.003.

A V58 usa uma noção diferente de bloco: todas as cláusulas que descrevem uma fibra de saída devem ser removidas ou reorientadas juntas. A prioridade dessa formulação em Range Avoidance não foi confirmada.

## 3. Fronteira do hipercubo

A relação entre bolas de Hamming e fronteiras pertence à geometria combinatória clássica do cubo. Harper caracteriza conjuntos de menor fronteira para cardinalidade fixada; trabalhos modernos estudam expansão local e estabilidade.

Referências próximas:

- Z. Jiang, A. Yehudayoff, *An Isoperimetric Inequality for Hamming Balls and Local Expansion in Hypercubes*, Electronic Journal of Combinatorics 29(1), 2022.
- P. Keevash, E. Long, *Stability for Vertex Isoperimetry in the Cube*, JCTB 145, 2020.

A equivalência elementar usada na V58 — ausência de fronteira até raio `r` implica inclusão da bola de raio `r+1` — não é reivindicada como novidade.

## 4. Hamming balls como imagens de circuitos locais

Benjamini, Cohen e Shinkar constroem uma bijeção bi-Lipschitz entre o cubo e uma bola de Hamming de metade do cubo, computável em `TC0`. Esse resultado é um alerta conceitual: imagens de tamanho `2^n` em `n+1` bits podem ter geometria muito semelhante a bolas grandes, embora a localidade por saída da V58 seja bem mais restritiva.

Referência:

- I. Benjamini, G. Cohen, I. Shinkar, *Bi-Lipschitz Bijection between the Boolean Cube and the Hamming Ball*, FOCS 2014 / Israel Journal of Mathematics 2016.

## 5. Posição da V58

A V58 não apresenta uma nova desigualdade isoperimétrica nem uma nova teoria geral de 2-CNF.

O conteúdo potencialmente reutilizável é a combinação:

```text
Range Avoidance
+ fibras bijuntivas por bloco
+ distância até a fronteira
+ entailment 2-CNF
+ censo normalizado de flip único
```

Prioridade externa permanece aberta.
