# Corrected Reproducibility Audit

**Audit date:** 2026-09-23  
**Target seasons:** 2023/2024, 2024/2025, 2025/2026  
**Forecast origins:** weeks 10, 12, 15, 18 and 20  
**Gate:** lambda=0.40, start=16  
**Scope:** corrected GitHub ASEC-G engine

## Executive result

**The corrected engine is deterministic and passes the target-season future-value mutation test. The national development MAE reproduces the previously observed approximately 301,098 value, but several other metrics differ materially from the older Pass4J/Pass6 scorecards.**

This means the GitHub implementation should **not** currently be described as an exact reproduction of the frozen Pass6D package.

## Corrected national scorecard

| Metric | Corrected result |
|---|---:|
| National case MAE | 301,097.7 |
| National case RMSE | 766,041.0 |
| Peak-week MAE | 0.733 weeks |
| Peak-incidence relative error | 27.57% |
| Cumulative-case relative error | 41.37% |
| Central 80% coverage | 79.24% |
| Central 90% coverage | 88.29% |
| Interval score, central 80% | 2.911M |
| Interval score, central 90% | 6.185M |

The MAE agrees with the earlier approximately 301,098 development result. The RMSE and probabilistic metrics should be treated as the authoritative results for the current GitHub implementation until reconciled against the frozen package.

## Additional corrected results

| Component | Result |
|---|---:|
| State case MAE | 79,378.3 |
| State hospitalisation MAE | 1,132.2 |
| State death MAE | 106.9 |

These are materially different from the earlier Pass4/Pass6 scorecard. This is evidence that the current GitHub engine is a simplified implementation rather than a byte-for-byte mirror of the frozen competition package.

## Reproducibility checks

### Determinism
**PASS.**

Repeated execution of every one of the 15 season/cutoff folds produced identical numerical outputs.

### Future-value mutation
**PASS.**

For every season and cutoff, target-season values after the cutoff were heavily perturbed and the forecasts were recomputed.

Maximum changes:
- national case forecasts: 0.0
- state case forecasts: 0.0
- case predictive quantiles: 0.0

This supports the absence of target-season future-case leakage in the audited case-forecast path.

### North/South aggregation
**PASS.**

North and South state forecasts sum to the complete state-level forecast to floating-point precision.

Maximum absolute discrepancy: 2.98e-08.

### Forecast coverage
All 15 rolling-origin folds were evaluated.

## Important reconciliation finding

The current GitHub implementation should **not** yet be used to claim the historical Pass6D scorecard wholesale.

The repository currently lacks several files from the frozen local research package, and the executable engine on GitHub produces materially different state/outcome metrics from the earlier frozen scorecard.

Therefore the publication workflow must now choose between:

1. **reconstructing the exact frozen Pass6D implementation on GitHub**, followed by reproduction of its original scorecard; or
2. **declaring the current GitHub engine the new canonical ASEC-G implementation**, then updating the report, validation artifacts and manuscript around its corrected results.

The first option is preferable for competition provenance; the second is appropriate only if the implementation differences are intentional methodological changes.

## Release decision

**No publication release tag yet.**

The repository has passed the core reproducibility tests for the current engine, but the implementation/provenance reconciliation must be completed before the repository can honestly claim to reproduce the frozen competition package.