# Teoremas — Laboratório V58

## Definição 1 — orientação e fórmula de fibra

Seja

\[
C:\{0,1\}^n\to\{0,1\}^m.
\]

Para uma palavra `y` de comprimento `m`, defina

\[
F_y(x)=\bigwedge_{i=1}^m [C_i(x)=y_i].
\]

No caso da órbita ternária NPN `0x07`, ambas as fibras locais são bijuntivas. Portanto cada bloco `[C_i(x)=y_i]` possui uma descrição 2-CNF de tamanho constante.

## Definição 2 — fronteira interna e profundidade de orientação

Para `S = Range(C)` e `b in S`, defina a fronteira interna

\[
\partial_{in}S=\{y\in S:\exists i,\ y\oplus e_i\notin S\}.
\]

A profundidade de orientação em torno de `b` é

\[
\rho_S(b)=\min_{y\in\partial_{in}S} d_H(b,y).
\]

## Teorema 1 — redundância equivale a uma aresta de fronteira

Se `y in S`, o bloco `i` é redundante em `F_y` se, e somente se,

\[
y\oplus e_i\notin S.
\]

Em outras palavras, procurar uma orientação consistente com um bloco redundante é exatamente procurar um vértice da fronteira interna da imagem.

## Teorema 2 — critério da bola de Hamming

Para todo inteiro `r >= 0`,

\[
\rho_S(b)>r
\quad\Longleftrightarrow\quad
B_H(b,r+1)\subseteq S.
\]

Em particular,

\[
\rho_S(b)>1
\quad\Longleftrightarrow\quad
B_H(b,2)\subseteq S.
\]

Assim, o método de um flip falha exatamente quando a imagem contém todos os padrões obtidos da orientação inicial por zero, um ou dois flips.

## Teorema 3 — algoritmo FPT por profundidade de orientação

Para circuitos cujas duas fibras de cada saída são 2-CNF, existe um algoritmo determinístico que, dado um limite `d`, encontra uma saída ausente sempre que

\[
\rho_S(b)\le d.
\]

O tempo é

\[
O\left(\left(\sum_{j=0}^{d}\binom mj\right)m\,\mathrm{poly}(n+m)\right).
\]

Para `d` constante, o algoritmo é polinomial.

O algoritmo enumera as orientações a distância no máximo `d` de `b`. Para cada uma:

1. testa consistência por 2-SAT;
2. se inconsistente, a própria orientação é uma saída ausente;
3. se consistente, testa entailment de cada bloco pelas demais fibras;
4. ao encontrar um bloco redundante, devolve a palavra vizinha obtida invertendo essa coordenada.

## Teorema 4 — limite universal por cardinalidade

Se `|S| <= 2^n`, então

\[
\rho_S(b)\le d-1,
\]

onde `d` é o menor inteiro tal que

\[
\sum_{j=0}^{d}\binom mj>2^n.
\]

No stretch mínimo `m=n+1`, isso dá

\[
\boxed{\rho_S(b)\le\lfloor n/2\rfloor.}
\]

Esse limite é geral, mas não fornece um algoritmo polinomial.

## Teorema computacional 5 — flip único até n=8 para a órbita 0x07

Considere circuitos homogêneos da órbita NPN `0x07`, com `m=n+1`, e a orientação em que cada porta seleciona sua fibra de três pontos.

Para

\[
3\le n\le 8,
\]

se a orientação inicial é consistente, então

\[
\rho_S(b)\le 1.
\]

Equivalentemente, a orientação inicial já possui um bloco redundante, ou algum flip único produz uma orientação inconsistente ou uma orientação com bloco redundante.

O resultado foi obtido por busca exata, não por amostragem. A normalização usa uma solução comum para transportar o alvo inicial a `0^n`. Cada fibra passa a ter a forma

\[
x_p=0
\quad\land\quad
(x_l,x_r)\ne f,
\qquad f\in\{01,10,11\}.
\]

O buscador enumera todas as famílias distintas, reduz os dois tipos possíveis para o primeiro bloco por simetria e utiliza apenas podas necessárias por capacidade das células de prefixo.

## Teorema 6 — reclassificação da barreira V57

As 12 famílias consistentes e irredundantes da V57 para `n=4,m=5`:

- formam uma única classe sob permutação das variáveis;
- possuem profundidade de orientação exatamente um;
- admitem 60 de 60 flips únicos bem-sucedidos;
- após cada flip, três ou quatro blocos tornam-se redundantes.

A família infinita por soma direta da V57 também possui profundidade exatamente um.

Portanto, a barreira V57 é uma barreira contra **orientação fixa**, não contra reorientação adaptativa de profundidade um.
