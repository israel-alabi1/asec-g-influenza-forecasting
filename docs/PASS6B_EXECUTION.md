# Pass 6B — Competition Forecast Engine

## Status
**PROVISIONAL / READY FOR SCHEMA ADAPTER**

The supplied challenge brief confirms the prediction targets and requires a forecast CSV, but does not publish the exact portal CSV schema. Therefore this package deliberately does not claim that its provisional CSV is portal-ready.

## Forecast levels
- Nigeria national
- North and South
- all 36 states + FCT

## Outcomes
- cases
- hospitalisations
- deaths

## Probabilistic output
- q05, q10, q25, q50, q75, q90, q95

## ASEC-G configuration
- late spatial gate lambda = 0.40
- gate start = week 16
- uncertainty early-horizon inflation = 0.20

These are development settings, not claims of an independently held-out test optimum.

## Integrity
Run:

```bash
python src/integrity_check.py submission/forecast_PROVISIONAL_*.csv
```

Before submission, replace the provisional writer with the organizer's exact schema and information-set rules.
