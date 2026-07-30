# Auditoria do flip único

## Conjectura testada

Para circuitos da órbita `0x07` com `m=n+1`, a orientação das fibras pequenas possui profundidade no máximo um.

## Reformulação exata

A conjectura falha se, e somente se, a imagem contém todas as palavras a distância zero, um e dois de `1^m`.

## Resultado certificado

A busca completa não encontrou contraexemplos para:

```text
n = 3, 4, 5, 6, 7, 8
m = n + 1
```

Foram considerados:

- todos os blocos normalizados contendo a solução comum `0^n`;
- os dois tipos possíveis para o primeiro bloco;
- suportes repetidos quando geram blocos diferentes;
- somente famílias de blocos distintos, pois blocos idênticos já são redundantes.

## Nós da busca

Os resultados completos estão em `EXACT_SEARCH_RESULTS.csv`.

```text
n=3,4,5: podados apenas pela capacidade da primeira fibra
n=6:      19 nós
n=7:   1.456 nós
n=8: 125.132 nós
```

Total reportado pelo verificador final: 126.607 nós.

## Caso n=9

Uma primeira busca em `n=9` utilizou uma redução de simetria incompleta. A auditoria detectou que impor índices maiores depois de fixar o segundo representante poderia omitir famílias.

A implementação foi corrigida, mas a busca completa em `n=9` não terminou no orçamento de validação desta versão.

Portanto:

```text
teorema exato: n <= 8
n = 9: aberto nesta infraestrutura
```
