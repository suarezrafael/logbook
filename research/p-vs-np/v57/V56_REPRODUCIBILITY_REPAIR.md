# Reparação de reprodutibilidade da V56

## Problema encontrado

O README da V56 indicava os comandos:

```bash
python verify.py
python verify_independent.py
```

mas a primeira publicação da pasta no GitHub não continha os dois verificadores completos. Apenas o verificador compacto de índice estava disponível.

Isso tornava não reproduzíveis, diretamente da branch, os números:

- 17.550 multisets da classe `0x06`;
- 3.876 multisets singleton;
- circuitos mistos e suportes repetidos;
- auditoria independente.

## Ação corretiva

Antes de promover a V57:

1. o pacote original da V56 foi reextraído;
2. `verify.py`, `verify_independent.py` e `verify_index.py` foram executados novamente;
3. os três passaram com zero falhas;
4. dois verificadores autocontidos foram publicados na mesma branch;
5. o padrão `OUTPUT_STANDARD.md` passou a proibir números não reproduzíveis no repositório.

## Resultados reexecutados

```text
14/14 classes NPN;
17.550 multisets 0x06;
3.876 multisets singleton;
350 misturas consistentes;
350 misturas não condicionadas;
210 casos de suportes repetidos;
720 testes abstratos de blocos;
zero falhas.
```

O teorema da V56 não foi alterado. A reparação é de publicação e reprodutibilidade.
