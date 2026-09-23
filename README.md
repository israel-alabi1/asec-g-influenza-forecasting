# MAEPiMS Challenge 2026 — ASEC-G Influenza Forecasting

## ASEC-G
**Adaptive Spatial Epidemic Clock with Gated Spatial Deformation** is an original forecasting framework developed for seasonal influenza forecasting from the supplied simulated national surveillance data.

The framework combines a latent national epidemic clock, regularized spatial phase deformation, secondary-wave propensity, a late gated spatial correction, outcome-specific severity transformations, and empirical log-scale uncertainty calibration.

### Current status
This repository contains the competition-development implementation and validation package. The current forecast files are **PROVISIONAL** because the supplied challenge brief did not publish the organizer's exact portal CSV schema or hidden-test information set.

### Reproduction

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the provisional forecast engine:

```bash
python src/forecast_engine.py \
  --data-dir <DATA_DIR> \
  --target-season 2025/2026 \
  --cutoff 20 \
  --output-dir submission/ \
  --gate-lambda 0.4 \
  --gate-start 16 \
  --uncertainty-inflation 0.20
```

Validate the generated forecast:

```bash
python src/integrity_check.py submission/forecast_PROVISIONAL_2025-2026_cutoff20.csv
```

### Development evidence
Rolling-origin development over the three supplied synthetic seasons reported:
- case MAE: 332,019
- RMSE: 689,518
- peak-week MAE: 0.60 weeks
- state case MAE: 10,106
- hospitalisation MAE: 144.8
- death MAE: 14.3
- central 80% coverage: 80.4%
- central 90% coverage: 88.8%

These are development results, not an independent hidden-test or leaderboard score.

### Repository structure
- `src/` — forecasting engine, adapter and validation code
- `docs/` — model specification, validation and competition-readiness documentation
- `submission/` — provisional forecast artifacts
- `validation/` — rolling-origin validation artifacts
- `report_figures/` — technical-report figures

### Important data convention
The supplied weekly CSVs encode `week_start` on Mondays, while the challenge brief describes epidemiological weeks as Sunday–Saturday. The pipeline preserves the supplied dates verbatim; the organizer's official portal instructions should determine the final submission convention.

### Competition
Developed for the **MAEPiMS Challenge 2026 — Nigeria Influenza Forecasting Challenge**. The repository is intentionally named after the ASEC-G method so that the implementation can support future research and publication independently of the competition.
