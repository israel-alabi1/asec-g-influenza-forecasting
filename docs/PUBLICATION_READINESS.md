# Publication Readiness Audit

**Repository:** ASEC-G Influenza Forecasting  
**Audit date:** 2026-09-23

## Current status

The repository is suitable as a **research-development repository**, but it should not yet be presented as a complete publication artifact.

### Completed

- Method name and acronym are stable: ASEC-G.
- Public repository identity is independent of the competition name.
- README distinguishes development evidence from hidden-test/leaderboard performance.
- Provisional submission schema is explicitly labelled.
- Reproduction commands are documented.
- A citation file and software license are included.
- Challenge dataset is not included in the public repository.
- The model specification and validation protocol are separated from competition documentation.

### Before manuscript submission

1. Add a complete mathematical specification of every fitted component and hyperparameter.
2. Add a formal ablation study isolating the epidemic clock, spatial phase deformation, secondary-wave propensity and gated correction.
3. Add comparisons against clearly defined statistical baselines using identical information sets.
4. Report forecast performance by season, forecast origin, horizon and geographic aggregation.
5. Separate parameter selection from final evaluation using an explicit nested or pre-specified procedure where feasible.
6. Expand uncertainty evaluation beyond marginal coverage to interval scores/WIS and calibration by horizon/regime.
7. Document the exact software environment and versions used for the final analysis.
8. Add tests for edge cases and explicit no-future-information guarantees.
9. Provide a reproducible script that regenerates every table and figure from the supplied data.
10. Add a manuscript DOI/citation once a paper or preprint is public.

## Important methodological review item

Only three synthetic seasons are available. Consequently, claims about generalisation, transfer to real influenza surveillance, or superiority across unseen epidemiological regimes require additional evidence and should not be inferred from the current development scorecard.
