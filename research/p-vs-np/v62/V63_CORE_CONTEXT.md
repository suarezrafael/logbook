# Contexto congelado para o Laboratório V63

## Fatos estáveis

1. A rota para P versus NP permanece encerrada.
2. O manuscrito integrado está em `v62/INTEGRATED_MANUSCRIPT.md`.
3. A narrativa central é V56 positivo versus V57 negativo.
4. V57 foi traduzido para IES: a fórmula colapsada é 2-CNF clause-irredundant; a estrutura específica é a partição em blocos de fibras da órbita `0x07`.
5. Kuntewar–Sarma 2025 subsume a conclusão algorítmica do V54 para `AND3` monotônico; a equivalência do certificado de grau quatro permanece aberta.
6. A busca não encontrou fonte exata para a formulação de blocos afins V56 nem para orientation depth. Isso não confirma novidade.
7. Dois e-mails foram enviados em 2026-07-30: um aos autores de Range Avoidance e outro a Paolo Liberatore.
8. O status externo é `sent_awaiting_reply`.
9. V22 continua `SKIP` por ausência de `full_certificate_cases.json`.
10. `n=9` continua apenas como falsificação e regressão.
11. Cada laboratório futuro deve ser publicado em um único commit coerente.
12. O V62 adiciona CI para executar `verify_all.sh` e `verify_all.sh --full`.

## Foco obrigatório

Aguardar e processar respostas externas sem paralisar o trabalho: revisar o manuscrito com base em evidência recebida e completar a validação em CI.

## Prioridades

1. Verificar o resultado do workflow completo do V62 e corrigir qualquer falha real.
2. Ler respostas aos dois e-mails, preservando remetente, contexto e distinção entre opinião e prova.
3. Atualizar `SOURCE_TO_CLAIM.json` quando uma referência direta for indicada.
4. Se não houver resposta, não reenviar antes de um intervalo razoável e não interpretar silêncio como confirmação.
5. Transformar o manuscrito em LaTeX somente depois de estabilizar alegações e referências.
6. Preparar apêndices reproduzíveis para V56, V57 e V58.
7. Manter V25 como material suplementar.
8. Não reabrir métricas de progresso rumo a P versus NP.

## Critérios de promoção

- CI quick e full sem falhas, com skips justificados;
- pelo menos uma resposta externa incorporada corretamente, ou registro explícito de que ainda está pendente;
- matriz fonte–alegação atualizada;
- nenhuma alegação de novidade ampliada sem evidência;
- manuscrito consistente com o ledger.
