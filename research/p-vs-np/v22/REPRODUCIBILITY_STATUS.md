# V22 reproducibility status

## Status

**Not reproducible from the committed repository as of V61.**

The standalone verifier accepts one positional argument: a directory containing

```text
full_certificate_cases.json
```

The file is not present in the V22 package or elsewhere in the pull-request tree.

## Why `RESULTS.json` is insufficient

`RESULTS.json` records only aggregate counts:

- 1,022 truth-table checks;
- 65 above-threshold circuits;
- 60 effective-rank circuits;
- 125 complete certificates;
- zero recorded failures.

The verifier needs, for each case:

- the complete circuit;
- every gate's variables and truth table by Hamming weight;
- dependency coefficients;
- normalized-output orientation;
- distinguished gate;
- selected missing output.

These data cannot be recovered uniquely from aggregate counts.

## Runner policy

`verify_all.sh` must print:

```text
V22 | primary | SKIP | missing v22/full_certificate_cases.json ...
```

It must not invoke `verify.py` without the required directory.

## Accepted future repairs

Any one of the following can close this issue:

1. recover and commit the original serialized dataset with provenance and hashes;
2. independently regenerate a new dataset and label it explicitly as a new reproduction, not the original 125 cases;
3. formally withdraw the historical finite-certificate count while retaining the human proof candidate.

Until one occurs, V22 remains a proof candidate without repository-executable finite evidence.
