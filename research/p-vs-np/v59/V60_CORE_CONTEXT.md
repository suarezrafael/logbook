# Contexto congelado para o Laboratório V60

## Fatos estáveis

1. As retratações da V53 permanecem válidas.
2. V56 resolve misturas de fibras afins no stretch mínimo.
3. V57 refuta redundância bijuntiva com orientação fixa.
4. V58 define profundidade de orientação e prova algoritmo FPT `m^{O(d)}`.
5. V58 conclui a busca exata do flip único até `n=8`; `n=9` permanece aberto.
6. V59 aplica Harper: a fronteira interna ocupa pelo menos `kappa_m=Theta(1/sqrt(m))` da imagem.
7. Se `alpha=|Range(C)|/2^n`, uma entrada uniforme atinge a fronteira com probabilidade pelo menos `kappa_m alpha`.
8. Amostragem uniforme da saída já dá Las Vegas esperado menor que duas tentativas quando a pertinência está em P; a fronteira determinística é o alvo real.
9. Na soma direta V57, o único interior e todos os vizinhos têm fibra unitária, `n` variáveis exatamente forçadas e zero propagação unitária.
10. Portanto, forced-count, unit-propagation e tamanho da fibra não fornecem melhora estrita universal.
11. A busca parcial `n=9` visitou 3.559.977 nós no tipo 1 e 2.637.185 no tipo 3, sem conclusão.
12. Existe um blueprint SAT Modulo Symmetries, mas ele ainda não foi implementado.

## Foco obrigatório

Transformar a busca `n=9` em geração canônica verificável e testar potenciais que atravessem platôs.

## Prioridades

1. Implementar a codificação SMS como grafo colorido variável–porta–incidência.
2. Adicionar testemunhas SAT de consistência e irredundância para baseline e flips.
3. Produzir prova DRAT ou certificado independentemente verificável.
4. Testar potenciais vetoriais baseados em SCCs, alcance e condensação do grafo de implicação.
5. Exigir que qualquer potencial novo passe pela família de soma direta V57.
6. Estudar caminhada com memória e tie-breaking canônico.
7. Separar claramente randomização trivial de progresso determinístico.
8. Contatar autores somente após autorização explícita.

## Critérios de promoção

- conclusão exata de `n=9` com prova verificável;
- contraexemplo explícito ao flip único;
- potencial determinístico provado para uma subclasse não trivial;
- barreira mínima contra toda uma família formal de potenciais;
- confirmação ou correção externa de prior art.
