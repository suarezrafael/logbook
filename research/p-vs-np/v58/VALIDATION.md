# Validação — V58

## Verificador principal

```text
96 reconstruções locais de fibras 2-CNF
12 famílias V57
1 classe de isomorfismo
60 flips únicos
família direta até k=12
1.100 circuitos aleatórios da órbita
900 equivalências fronteira/bola
600 limites universais
0 falhas
```

## Verificador independente

```text
12 famílias reconstruídas sem importar o núcleo
1 classe de isomorfismo
60 flips únicos
busca exata independente para n=3..7
500 equivalências fronteira/bola
0 falhas
```

## Verificador exato C++

```text
n=3..8
2 tipos canônicos para o primeiro bloco
126.607 nós DFS
0 contraexemplos
busca completa
```

## Testes defensivos incorporados

- validação da descrição 2-CNF contra cada tabela-verdade local;
- comparação de entailment com ausência real no range;
- blocos repetidos tratados como redundância imediata;
- dois tipos de primeiro bloco após normalização;
- redução do segundo bloco somente pelo estabilizador do primeiro;
- enumeração dos blocos restantes sobre toda a lista, evitando a falha de simetria detectada durante a V58;
- `n=9` explicitamente excluído do teorema.
