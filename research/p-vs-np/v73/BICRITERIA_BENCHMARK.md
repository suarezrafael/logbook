# Exact bicriteria benchmark

The table compares the exact minimum projected cost at the smallest feasible frontier budget `q*` with the unrestricted exact optimum `G*_proj`.

| Frozen record | `q*` | cost at `q*` | `G*_proj` | minimum budget attaining `G*_proj` | slack | price of minimum width |
|---|---:|---:|---:|---:|---:|---:|
| V69 natural `n=6` | 4 | 18 | 15 | 6 | 2 | 1.200 |
| V69 natural `n=8` | 4 | 16 | 15 | 5 | 1 | 1.067 |
| V69 natural `n=10` | 4 | 24 | 17 | 7 | 3 | 1.412 |
| V69 natural `n=12` | 4 | 52 | 29 | 7 | 3 | 1.793 |
| V70 exact record `n=8` | 4 | 31 | 29 | 6 | 2 | 1.069 |
| V70 exact record `n=10` | 5 | 32 | 30 | 7 | 2 | 1.067 |

The maximum observed exact price is `52/29 = 1.793103...`. On these six finite records, allowing one to three extra frontier variables is sufficient to attain the unrestricted residual optimum.

This is finite evidence only. It is not an approximation theorem and does not imply a universal bound between the two objectives.
