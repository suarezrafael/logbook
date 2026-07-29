# Provas da V57

## 1. Forcing universal de borda

Considere o grafo do hipercubo `{0,1}^m`, em que dois pontos são adjacentes quando diferem em um bit.

Se um subconjunto não vazio `S` não possuísse nenhuma aresta saindo de `S`, então, para todo `y in S` e toda coordenada `i`, o vizinho `y xor e_i` também pertenceria a `S`.

Como o hipercubo é conexo, a partir de qualquer ponto de `S` poderíamos alcançar todos os pontos por sucessivos flips. Portanto `S` seria o cubo inteiro, contradizendo a hipótese de que é próprio.

Logo existe `y in S` e `i` com `y xor e_i notin S`.

Os dois pontos têm o mesmo contexto `y_{-i}`. Como o vizinho de bit oposto não pertence a `S`, esse contexto força o valor `y_i` dentro de `S`.

## 2. Verificação do gadget de cinco blocos

Os blocos são:

```text
B1 = ¬x0 ∧ (¬x1 ∨  x2)
B2 = ¬x0 ∧ ( x1 ∨ ¬x2)
B3 = ¬x0 ∧ (¬x1 ∨  x3)
B4 = ¬x0 ∧ ( x1 ∨ ¬x3)
B5 = ¬x0 ∧ (¬x2 ∨ ¬x3).
```

### 2.1 Pertencimento à órbita 0x07

Cada bloco fixa uma variável e proíbe uma única atribuição das outras duas. Sua fibra possui três pontos numa face bidimensional do cubo, exatamente o tipo de fibra pequena da órbita NPN `0x07`.

As máscaras locais são:

```text
B1: 0x51 on (x0,x1,x2)
B2: 0x45 on (x0,x1,x2)
B3: 0x51 on (x0,x1,x3)
B4: 0x45 on (x0,x1,x3)
B5: 0x15 on (x0,x2,x3).
```

A enumeração das 48 transformações NPN confirma o pertencimento.

### 2.2 Consistência e unicidade

`B1` e `B2` juntos impõem `x1=x2`.

`B3` e `B4` juntos impõem `x1=x3`.

`B5` proíbe `x2=x3=1`.

Todos os blocos impõem `x0=0`. Assim:

```text
x0=x1=x2=x3=0.
```

Logo a interseção é exatamente `{0000}`.

### 2.3 Irredundância

As testemunhas abaixo satisfazem todos os blocos exceto o indicado:

```text
sem B1: 0101
sem B2: 0010
sem B3: 0110
sem B4: 0001
sem B5: 0111
```

A ordem dos bits é `(x0,x1,x2,x3)`.

Portanto nenhum `B_i` é consequência da conjunção dos outros quatro.

## 3. Componentes fortemente conexas

Cada cláusula binária `(a ∨ b)` gera as implicações `¬a -> b` e `¬b -> a`. As unidades `¬x0` geram `x0 -> ¬x0`.

No sistema completo, as SCCs são:

```text
{x0},
{¬x0},
{x1,x2,x3},
{¬x1,¬x2,¬x3}.
```

Há quatro SCCs, enquanto existem cinco blocos. Apesar disso, todos os blocos são essenciais. Assim, a regra `m > número de SCCs => bloco redundante` é falsa.

A fórmula também possui solução única, portanto todas as variáveis são forçadas; mesmo assim, não há bloco redundante.

## 4. Minimalidade finita

Com três variáveis e portas ternárias essenciais de entradas distintas, todas as portas têm o mesmo suporte.

A órbita NPN de `0x07` contém 48 tabelas. Considerando a fibra pequena de cada tabela e circuitos com quatro saídas, permutar as coordenadas de saída não altera consistência ou redundância. Logo basta enumerar multisets:

```text
C(48+4-1,4)=249.900.
```

O resultado exato foi:

```text
206.280 inconsistentes;
43.620 consistentes com pelo menos um bloco redundante;
0 consistentes completamente irredundantes.
```

Isso prova minimalidade dentro do modelo finito especificado, com a ressalva de que é uma certificação computacional exaustiva.

## 5. Família assintótica

O gadget balanceado de três variáveis usa as máscaras:

```text
0x07, 0x0b, 0x0d
```

no mesmo suporte. Suas fibras pequenas têm interseção `{000}` e cada uma possui uma testemunha de irredundância.

Tome uma cópia do gadget `G4` de quatro variáveis e cinco blocos, mais `k` cópias disjuntas do gadget balanceado `G3`.

Então:

```text
n=4+3k,
m=5+3k=n+1.
```

A atribuição zero satisfaz todos os blocos. Para mostrar que um bloco continua essencial, use sua testemunha local e mantenha todas as outras componentes na atribuição zero. Logo nenhum bloco é redundante.

## 6. Por que isso não resolve Avoid

O contraexemplo derruba apenas o algoritmo que:

1. escolhe previamente a fibra pequena de todas as portas `0x07`;
2. testa inconsistência;
3. caso consistente, exige que algum bloco completo seja implicado pelos demais.

Outras escolhas de orientação ou métodos de busca continuam possíveis. O forcing de borda garante que algum contexto completo existe, mas não ensina como encontrá-lo eficientemente a partir da descrição local do circuito.
