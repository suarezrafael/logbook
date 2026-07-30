# Contexto congelado para o Laboratório V62

## Fatos estáveis

1. A rota para P versus NP permanece encerrada.
2. O artigo deve ser construído em torno da dicotomia V56/V57.
3. V25 é material suplementar, não parte do núcleo narrativo.
4. V22 não é reproduzível a partir do repositório porque `full_certificate_cases.json` está ausente.
5. O runner deve registrar V22 como `SKIP` com motivo explícito.
6. Irredundância geral de CNF e 2-CNF é prior art.
7. UCP-irredundância também é prior art.
8. O algoritmo aleatório do V60 é contexto elementar, não novidade.
9. Kuntewar–Sarma 2025 resolve `MONOTONE-NC0_3-Avoid` para `m>n`; V54 precisa de comparação explícita.
10. A novidade exata de V56, da construção orbit-constrained V57 e da profundidade de orientação permanece não confirmada.
11. O contato externo continua não enviado.
12. `n=9` continua apenas como falsificação e regressão.

## Foco obrigatório

Produzir um rascunho integrado do artigo e um pacote de revisão externa, sem ampliar alegações.

## Prioridades

1. Escrever introdução e seção de trabalhos relacionados com citações primárias.
2. Traduzir V57 para a terminologia padrão de irredundant equivalent subsets e explicar a restrição por órbita NPN.
3. Comparar V54 formalmente com Kuntewar–Sarma.
4. Buscar prior art específica para sistemas afins agrupados e para orientation depth.
5. Rodar `verify_all.sh --full` em ambiente limpo.
6. Decidir se V22 será recuperado, reproduzido como novo experimento ou mantido como dívida histórica.
7. Preparar pedido de revisão, mas não enviar sem autorização explícita.

## Critérios de promoção

- manuscrito integrado com alegações alinhadas ao ledger;
- tabela source-to-claim completa;
- zero falhas no runner e skips justificados;
- pelo menos um parecer externo, somente após autorização para contato;
- nenhuma reivindicação de novidade sem suporte.
