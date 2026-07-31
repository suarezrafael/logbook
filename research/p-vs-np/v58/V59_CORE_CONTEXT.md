# Contexto congelado para o Laboratório V59

## Fatos estáveis

1. As retratações da V53 permanecem válidas.
2. V56 resolve misturas de fibras afins para `m>n`.
3. V57 refuta redundância bijuntiva com orientação fixa.
4. V58 define profundidade de orientação como distância até a fronteira interna da imagem.
5. Para fibras 2-CNF, profundidade `d` fornece algoritmo `m^{O(d)} poly(n+m)`.
6. Profundidade maior que `r` equivale à inclusão da bola de Hamming de raio `r+1`.
7. No stretch um, a profundidade universal é no máximo `floor(n/2)` por cardinalidade.
8. As 12 famílias finitas V57 são uma única classe de isomorfismo.
9. Todos os 60 flips dessas famílias funcionam.
10. A família infinita V57 possui profundidade exatamente um.
11. A busca exata não encontrou contraexemplo ao flip único para `n=3..8`.
12. `n=9` não foi concluído e permanece aberto.
13. O contato de prior art está atualizado, mas não enviado.

## Foco obrigatório

Decidir se a profundidade de orientação da órbita `0x07` é universalmente limitada.

## Rotas prioritárias

1. Concluir a busca exata em `n=9` com dois solvers independentes.
2. Formular a falha do flip único como existência de todas as testemunhas de zero-set de tamanho até dois.
3. Relacionar essas testemunhas a famílias cover-free de subcubos de codimensão baixa.
4. Provar um bound extremal para blocos `unit + binary clause`.
5. Testar profundidade dois em qualquer candidato que sobreviva ao flip único.
6. Procurar construção assintótica com profundidade crescente.
7. Estudar `0x17` e `0x1b` com a mesma medida.
8. Enviar o contato de prior art somente após autorização explícita.

## Critérios de promoção

- prova de profundidade constante para `0x07`;
- contraexemplo explícito ao flip único;
- família com profundidade crescente;
- algoritmo FPT por parâmetro estrutural menor que a profundidade bruta;
- conclusão exata de `n=9` por verificadores independentes;
- confirmação ou correção externa de prior art.
