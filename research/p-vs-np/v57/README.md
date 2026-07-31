# Laboratório P versus NP — V57

## Fronteira bijuntiva: forcing de borda e barreira à redundância de blocos

**Estado científico:** pacote interno, reproduzível e auditado por duas implementações independentes. Não revisado por pares. A prioridade bibliográfica dos resultados específicos para Range Avoidance não está confirmada. A literatura anterior já estuda redundância e subconjuntos irredundantes de fórmulas 2-CNF; portanto, a V57 não reivindica novidade para a noção lógica de irredundância.

A V57 não resolve `NC0_3-Avoid` geral, não prova lower bounds irrestritos e não resolve P versus NP.

## Resultado central

A analogia direta com a V56 é falsa para blocos bijuntivos.

Na V56, depois de verificar consistência, mais blocos afins que a dimensão linear forçam um bloco redundante. Na V57 construímos cinco portas da mesma órbita NPN ternária `0x07`, em quatro variáveis, tais que:

- todas as fibras ativas são 2-CNF e têm três pontos;
- a conjunção das cinco fibras é consistente e possui solução comum única;
- nenhuma fibra é implicada pelas outras quatro;
- o grafo de implicação completo possui apenas quatro SCCs, mas os cinco blocos continuam essenciais;
- todas as quatro variáveis ficam forçadas, mas nenhum bloco pode ser removido.

Assim, nem a quantidade de variáveis, nem a contagem simples de SCCs, nem a quantidade de variáveis forçadas fornece um substituto direto para o posto linear da V56.

## Contraexemplo explícito

Com variáveis `x0,x1,x2,x3`, os cinco blocos ativos são:

```text
B1 = ¬x0 ∧ (¬x1 ∨  x2)
B2 = ¬x0 ∧ ( x1 ∨ ¬x2)
B3 = ¬x0 ∧ (¬x1 ∨  x3)
B4 = ¬x0 ∧ ( x1 ∨ ¬x3)
B5 = ¬x0 ∧ (¬x2 ∨ ¬x3)
```

Eles correspondem às máscaras e suportes:

```text
0x51 on (0,1,2)
0x45 on (0,1,2)
0x51 on (0,1,3)
0x45 on (0,1,3)
0x15 on (0,2,3)
```

Todas as máscaras pertencem à órbita NPN de `0x07`.

A solução comum é `0000`. Cada bloco é indispensável; ao removê-lo existe uma testemunha que satisfaz os outros quatro e viola exatamente esse bloco.

## Família assintótica

O gadget de cinco blocos pode ser combinado com componentes balanceados de três variáveis e três blocos. Para todo `k>=0`, obtemos:

```text
n = 4 + 3k
m = 5 + 3k = n + 1
```

Todos os blocos pertencem à órbita `0x07`, todas as fibras pequenas escolhidas são conjuntamente consistentes e nenhum bloco é redundante.

Portanto, a falha da analogia de redundância não é apenas um fenômeno pequeno.

## O forcing observado em circuitos aleatórios

A observação de que “alguma porta é forçada pelas outras `m-1`” é verdadeira para qualquer imagem booleana própria, não apenas para `0x07`.

Todo subconjunto não vazio e próprio do hipercubo possui uma aresta de fronteira. Se `y` está na imagem e `y⊕e_i` não está, então o contexto `y_{-i}` força o bit `y_i` dentro da imagem.

Esse resultado é existencial. Encontrar eficientemente a aresta de fronteira continua sendo a dificuldade algorítmica; a experiência aleatória, por si só, não fornece uma medida computável equivalente ao posto.

## Validação

```bash
python verify.py
python verify_independent.py
```

Resultados esperados:

```text
65.804 subconjuntos próprios de cubos verificados;
249.900 multisets n=3,m=4 da órbita 0x07 examinados;
376.992 famílias normalizadas n=4,m=5 examinadas;
12 famílias consistentes e completamente irredundantes encontradas;
família assintótica verificada estruturalmente até k=20;
dois verificadores; zero falhas.
```

## Padrão obrigatório de saída restaurado

A partir da V57, cada laboratório deve conter no repositório, e não apenas na mensagem final:

1. estado científico e limite de novidade;
2. teorema e prova;
3. ataques de falsificação e contraexemplos;
4. validação primária e independente;
5. resumo para leigos;
6. índice de promoção e decisão explícita;
7. índices de progresso;
8. distância até P versus NP;
9. pesquisa bibliográfica primária;
10. contexto congelado da próxima versão;
11. manifesto e hashes reproduzíveis.

Veja `OUTPUT_STANDARD.md`.
