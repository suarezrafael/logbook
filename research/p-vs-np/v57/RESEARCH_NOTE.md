# Nota de pesquisa — V57

## Pergunta inicial

A V56 resolve fibras afins usando uma dicotomia:

```text
inconsistência global ou redundância de um bloco linear.
```

A V57 perguntou se, para fibras bijuntivas, a consistência de mais blocos que variáveis também forçaria uma fibra completa a ser consequência das outras.

## Resposta

Não.

A família explícita de cinco blocos 2-CNF em quatro variáveis é consistente, possui solução única e é completamente irredundante. O fenômeno persiste numa família stretch-one infinita dentro da órbita NPN `0x07`.

## Lição metodológica

No caso afim, todas as consequências vivem num matroide linear e podem ser medidas por posto.

No caso 2-CNF, consequências surgem por alcançabilidade dirigida. Uma fórmula pode forçar todas as variáveis e ainda depender essencialmente de cada bloco. O número de SCCs não mede a quantidade de blocos essenciais.

## Nova pergunta operacional

A V58 não deve procurar um simples número `rho` com a regra:

```text
m > rho => bloco redundante.
```

Ela deve procurar estruturas localizáveis que produzam um alvo ausente, por exemplo:

- pares de caminhos contraditórios;
- dominadores no grafo de implicação;
- cortes que isolam uma orientação de saída;
- branching limitado entre as duas células afins de uma fibra;
- núcleos mínimos após escolhas adaptativas.
