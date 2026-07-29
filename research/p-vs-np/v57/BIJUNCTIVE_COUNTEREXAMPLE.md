# Certificado explícito da barreira bijuntiva

## Portas

| Bloco | Máscara | Suporte | Fibra ativa (2-CNF) |
|---|---:|---|---|
| B1 | `0x51` | `(0,1,2)` | `¬x0 ∧ (¬x1 ∨ x2)` |
| B2 | `0x45` | `(0,1,2)` | `¬x0 ∧ (x1 ∨ ¬x2)` |
| B3 | `0x51` | `(0,1,3)` | `¬x0 ∧ (¬x1 ∨ x3)` |
| B4 | `0x45` | `(0,1,3)` | `¬x0 ∧ (x1 ∨ ¬x3)` |
| B5 | `0x15` | `(0,2,3)` | `¬x0 ∧ (¬x2 ∨ ¬x3)` |

Todas pertencem à órbita NPN `0x07` e usam a fibra de tamanho três como estado ativo.

## Solução comum

```text
0000
```

## Testemunhas de irredundância

| Bloco removido | Testemunha `(x0,x1,x2,x3)` |
|---|---|
| B1 | `0101` |
| B2 | `0010` |
| B3 | `0110` |
| B4 | `0001` |
| B5 | `0111` |

Cada testemunha viola o bloco removido e satisfaz os outros quatro.

## Consequência

A família é consistente, possui solução única e ainda assim é completamente irredundante. Logo a redundância de blocos afins da V56 não se transfere diretamente para 2-CNF.
