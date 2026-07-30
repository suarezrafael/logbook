# Demonstrações da V59

Este arquivo demonstra os resultados promovidos na V59 e separa cuidadosamente os fatos derivados de Harper, as consequências algorítmicas e os resultados negativos sobre caminhadas locais.

## 1. Fronteira interna e redundância

Para uma imagem `S` no cubo de saída, um ponto `y in S` está na fronteira interna quando existe uma coordenada `i` tal que `y xor e_i` não pertence a `S`. Em circuitos com fibras bijuntivas, a pertinência de cada orientação é decidida por 2-SAT. Assim, dado `y in S`, testar todas as `m` orientações vizinhas encontra uma saída ausente sempre que `y` está na fronteira.

## 2. Corolário isoperimétrico

A forma vertex-isoperimétrica do teorema de Harper diz que, entre subconjuntos do hipercubo com cardinalidade fixada, segmentos iniciais da ordem simplicial minimizam a vizinhança externa. Para conjuntos de tamanho no máximo metade do cubo, a comparação com a meia-bola fornece

```text
|∂in S| / |S| >= binom(m,floor(m/2))/2^(m-1).
```

Pela aproximação central de Stirling, o lado direito é `Theta(1/sqrt(m))`.

## 3. Amostragem por entradas

Se `alpha=|S|/2^n`, cada ponto da fronteira tem pelo menos uma preimagem. Logo a massa da fronteira sob a distribuição induzida por uma entrada uniforme é pelo menos

```text
|∂in S|/2^n >= kappa_m |S|/2^n = kappa_m alpha.
```

Quando `alpha` é inversamente polinomial e a pertinência à imagem é polinomial, isso fornece localização randomizada da fronteira em tempo esperado `O(sqrt(m)/alpha)` amostras, seguida de no máximo `m` testes de vizinhos.

## 4. Limite do resultado randomizado

No regime `m>n`, uma palavra uniforme do cubo de saída já está fora da imagem com probabilidade pelo menos `1/2`. Portanto, quando a pertinência pode ser testada em P, a amostragem direta de saídas é um algoritmo Las Vegas ainda mais simples. A isoperimetria é promovida como uma descrição da geometria e como uma ferramenta para localização a partir de pontos conhecidos da imagem, não como a melhor randomização geral.

## 5. Platô da família de soma direta

A família da V57 é uma soma direta de um gadget-base e componentes independentes. Na orientação canônica, cada componente tem uma única atribuição compatível. Assim, a orientação global `1^m` tem uma única preimagem e força todas as variáveis.

Ao alterar uma única coordenada de saída, a fórmula ainda possui uma única preimagem e continua forçando todas as variáveis; entretanto, o novo ponto já está na fronteira. A descrição 2-CNF usada não contém cláusulas unitárias iniciais, de modo que propagação unitária sem decisão força zero variáveis tanto no centro quanto nos vizinhos.

Portanto, os três potenciais são constantes na primeira aresta:

```text
preimage size = 1;
forced variables = n;
unit-propagated variables = 0.
```

Isso refuta qualquer prova de caminhada que exija melhora estrita de um desses valores em toda etapa interior.

## 6. Busca exata n=9

O verificador C++ da V58 foi reconstruído e executado separadamente para os dois tipos canônicos de primeiro bloco, com limite de 100.000 nós por ramo e oito threads. Nenhum contraexemplo foi localizado, mas ambos os processos atingiram limites internos; logo os resultados são incompletos e não possuem força de teorema.

## 7. SAT Modulo Symmetries

A codificação proposta representa a existência de um circuito contraprova e de testemunhas para o baseline e cada flip. A condição de ausência de bloco redundante também é codificada por uma testemunha que satisfaz os demais blocos e viola o bloco considerado. O objeto possui simetrias de variáveis, portas e terminais locais. SMS pode testar canonicidade durante a busca CDCL, evitando a redução estática incorreta detectada anteriormente. Nenhuma execução SMS ou prova DRAT é reivindicada na V59.
