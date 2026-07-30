# Estado científico — Laboratório V59

## Status geral

Pacote de pesquisa interno, reproduzível e adversarialmente auditado. Não passou por revisão por pares. Nenhuma prioridade bibliográfica é reivindicada.

A V59 não resolve `0x07-Avoid` de forma determinística, não resolve `NC0_3-Avoid`, não prova lower bounds irrestritos e não resolve P versus NP.

## Resultados internamente demonstrados

1. Para uma imagem `S ⊆ {0,1}^m` com `|S| ≤ 2^(m-1)`, o teorema isoperimétrico de Harper implica que a fronteira interna contém uma fração `Theta(1/sqrt(m))` de `S` no pior caso.
2. Para um circuito `C:{0,1}^n->{0,1}^m`, uma entrada uniforme atinge a fronteira com probabilidade pelo menos `kappa_m * alpha`, onde `alpha=|Range(C)|/2^n` e `kappa_m=binom(m,floor(m/2))/2^(m-1)`.
3. Em circuitos cujas fibras de saída são bijuntivas, um ponto de fronteira produz uma saída ausente com `m` testes de 2-SAT.
4. A família de soma direta da V57 possui um único ponto interior, mas três potenciais naturais são planos entre esse ponto e todos os seus vizinhos: número exato de variáveis forçadas, propagação unitária e tamanho exato da fibra.
5. A busca exata antiga para `n=9` foi executada com limite de ramos. Nenhum contraexemplo foi encontrado, mas a busca não foi concluída.
6. Foi preparado um plano de codificação SAT Modulo Symmetries para uma busca livre de isomorfismos e com caminho para prova DRAT.

## Resultados conhecidos ou essencialmente folclóricos

- A desigualdade de fronteira vem do teorema clássico de Harper.
- Amostrar uma palavra de saída uniforme e testar pertinência já fornece um algoritmo Las Vegas esperado em menos de duas tentativas quando a pertinência à imagem está em P. Para fibras 2-CNF, o teste é 2-SAT. Portanto, a isoperimetria não é necessária para o caso randomizado irrestrito de `0x07-Avoid`.
- O valor da V59 está na separação conceitual entre abundância e localização determinística, na barreira aos potenciais e no plano de busca exata.

## Não demonstrado

- uma caminhada determinística de comprimento polinomial até a fronteira;
- uma função potencial estritamente crescente em todo ponto interior;
- profundidade de orientação universalmente constante;
- conclusão exata do caso `n=9`;
- novidade da formulação de localização de fronteira.

## Decisão de promoção

Promovido como **resultado geométrico/algorítmico parcial e barreira negativa**, não como avanço determinístico geral.
