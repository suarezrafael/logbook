# Demonstrações — Laboratório V58

## 1. Redundância e fronteira

Fixe uma palavra `y in Range(C)` e uma coordenada `i`.

O bloco `i` é redundante em `F_y` quando

\[
\bigwedge_{j\ne i}[C_j(x)=y_j]
\implies [C_i(x)=y_i].
\]

Isso é equivalente a afirmar que não existe `x` com

\[
C_j(x)=y_j\quad(j\ne i),
\qquad C_i(x)=1-y_i.
\]

A palavra produzida por tal entrada seria exatamente `y xor e_i`. Logo o bloco é redundante se, e somente se, essa palavra vizinha não pertence à imagem.

## 2. Bola de Hamming e profundidade

### Direção direta

Suponha `rho_S(b)>r`. Se faltasse um ponto `z` da bola de raio `r+1`, tome um caminho mínimo no hipercubo de `b` até `z`.

Como `b in S` e `z notin S`, existe a primeira aresta que sai de `S`. Seu primeiro vértice pertence à fronteira interna e está a distância no máximo `r` de `b`, contradizendo a hipótese.

Portanto toda a bola de raio `r+1` está contida em `S`.

### Direção inversa

Se a bola de raio `r+1` está em `S`, todo ponto de `S` a distância no máximo `r` de `b` possui todos os seus vizinhos ainda dentro dessa bola. Nenhum deles pertence à fronteira interna. Assim `rho_S(b)>r`.

## 3. Algoritmo bijuntivo

As relações da órbita `0x07` possuem três pontos numa fibra e cinco na outra. Ambas são relações bijuntivas e podem ser reconstruídas pela conjunção de todas as cláusulas unitárias e binárias válidas nelas.

Para uma orientação `y`, a fórmula `F_y` é uma 2-CNF com `O(m)` cláusulas.

- Consistência é decidida em tempo linear pelo grafo de implicações e SCCs.
- Para testar se uma fórmula `G` implica uma cláusula `(a or b)`, testa-se a insatisfatibilidade de `G and not a and not b`.
- Cada bloco possui tamanho constante; portanto a redundância dos `m` blocos é testada com `O(m)` chamadas de 2-SAT.

Enumerando a bola de orientações de raio `d`, obtemos o tempo declarado.

## 4. Limite universal

Se não existe fronteira até distância `r`, o Teorema 2 força a inclusão de toda a bola de raio `r+1` na imagem.

A imagem possui no máximo `2^n` pontos. Logo a primeira bola cujo tamanho excede `2^n` não pode estar contida na imagem.

Quando `m=n+1`, `2^n=2^{m-1}`. Pela simetria dos coeficientes binomiais, a primeira bola estritamente maior que metade do cubo tem raio:

- `(m+1)/2` quando `m` é ímpar;
- `m/2` quando `m` é par.

Subtraindo um para obter a distância da fronteira, resulta `floor(n/2)`.

## 5. Correção da busca exata

### Normalização

Considere a orientação das fibras pequenas e suponha que ela seja consistente. Escolha uma entrada comum `x*`. Complemente cada variável para transportar `x*` a `0^n`.

Toda fibra pequena da órbita `0x07` torna-se um L de três pontos contendo a origem. Ela possui exatamente uma coordenada fixada em zero e exclui um dos três padrões não nulos em duas coordenadas restantes:

\[
x_p=0\land(x_l,x_r)\ne f,
\quad f\in\{01,10,11\}.
\]

Blocos idênticos podem ser excluídos: a repetição já produz redundância na orientação inicial.

### Critério pesquisado

Pelo Teorema 2, um contraexemplo ao flip único deve conter toda a bola de raio dois em torno de `1^m`.

Ao selecionar `t` blocos, uma célula de prefixo com `z` zeros precisa conter pelo menos

\[
R(m,t,z)=\sum_{q=0}^{2-z}\binom{m-t}{q}
\]

entradas distintas, pois esse é o número de palavras completas da bola de raio dois que estendem o prefixo.

Se a célula possui menos entradas, nenhuma extensão posterior da família poderá reparar a deficiência. A poda é, portanto, necessária e não remove soluções válidas.

### Simetria

O primeiro bloco pode ser transportado por permutação das variáveis para um de dois tipos:

- padrão proibido de peso um, representado por `f=01`;
- padrão proibido de peso dois, `f=11`.

O buscador verifica ambos. A segunda redução utiliza somente o estabilizador do primeiro bloco. Depois de fixar um representante da órbita do segundo bloco, os blocos restantes são novamente enumerados sobre a lista inteira, em ordem crescente e excluindo os já escolhidos. Essa última condição evita a omissão que ocorreria se a busca começasse apenas depois do índice do representante.

A versão final executou 126.607 nós completos para `n=3,...,8` e não encontrou família contendo a bola de raio dois.

## 6. Gadget V57

O censo independente das 376.992 famílias normalizadas de cinco blocos em quatro variáveis encontra 12 famílias consistentes e irredundantes.

A canonização por todas as 24 permutações das variáveis produz a mesma assinatura para as 12 famílias.

Para cada uma das 12 famílias e cada uma das cinco coordenadas:

1. a orientação com esse único bloco complementado continua consistente, como já decorre da irredundância original;
2. o teste de entailment encontra três ou quatro blocos redundantes;
3. inverter uma dessas coordenadas redundantes produz uma palavra ausente.

Na soma direta, o gadget de quatro variáveis permanece como componente. O mesmo flip e a mesma implicação interna continuam válidos independentemente dos componentes adicionais. Logo a profundidade permanece um para todo `k`.
