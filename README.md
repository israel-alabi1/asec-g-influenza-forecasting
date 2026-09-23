# ASEC-G: Adaptive Spatial Epidemic Clock with Gated Spatial Deformation

**ASEC-G** is an original forecasting framework for seasonal influenza surveillance data, developed and evaluated on the simulated Nigeria dataset supplied for the **MAEPiMS Challenge 2026**.

> **Research status:** This repository is a competition-development and research artifact. Reported performance numbers are rolling-origin development results unless explicitly labelled otherwise. They are not independent hidden-test or leaderboard results.

## Method at a glance

ASEC-G decomposes the forecasting problem into:

1. **Latent epidemic clock** — a smoothed national log-case trajectory represents the shared temporal epidemic signal.
2. **Spatial phase deformation** — state trajectories are aligned to the common clock through temporal shifts.
3. **Secondary-wave propensity** — observed state-level level, slope, acceleration and cumulative activity provide a weak signal for later-wave amplitude.
4. **Gated spatial correction** — the state-level component is introduced gradually through a late-season logistic gate.
5. **Outcome transformation** — hospitalisations and deaths are derived from case forecasts using healthcare-access and zone information.
6. **Log-scale uncertainty** — predictive quantiles are constructed from historical out-of-sample log residuals.

See docs/asec_model_spec.md for the formal model description.

## Current repository status

This is the publication-oriented development copy of ASEC-G. The MAEPiMS submission adapter remains provisional because the organizer's exact portal CSV schema and hidden-test information set were not included in the supplied challenge brief.

## Reproducibility

Install:

    python -m pip install -r requirements.txt

Run ASEC-G:

    python src/forecast_engine.py --data-dir <DATA_DIR> --target-season 2025/2026 --cutoff 20 --output-dir outputs --gate-lambda 0.4 --gate-start 16 --uncertainty-inflation 0.20

Validate:

    python src/integrity_check.py outputs/forecast_PROVISIONAL_2025-2026_cutoff20.csv

See docs/VALIDATION_PROTOCOL.md for the validation design.

## Development evidence

| Metric | Development result |
|---|---:|
| National case MAE | 332,019 |
| National case RMSE | 689,518 |
| Peak-week MAE | 0.60 weeks |
| State case MAE | 10,106 |
| Hospitalisation MAE | 144.8 |
| Death MAE | 14.3 |
| Central 80% coverage | 80.4% |
| Central 90% coverage | 88.8% |

These results use the supplied three synthetic seasons and multiple pseudo-real-time forecast origins. Because only three seasons are available, they are development evidence rather than evidence of external generalisation.

A later parameter-search result around 301,098 national case MAE was treated as same-fold model-selection evidence and is not reported as an independent test result.

## Data-use policy

ASEC-G was developed under the MAEPiMS rule that the forecasting model must use only the supplied simulated surveillance dataset. The repository does not require external epidemiological data.

Do not commit the supplied challenge dataset to this public repository unless the organizer explicitly permits redistribution.

## Repository structure

- src/ — forecasting engine, adapter and validation code
- docs/ — model specification, validation and publication documentation
- validation/ — rolling-origin validation artifacts
- submission/ — provisional competition forecast artifacts
- report_figures/ — publication/report figures

## Publication direction

The intended research contribution is the combination of a shared epidemic clock, interpretable spatial phase deformation, weak secondary-wave propensity and late gated spatial correction.

The repository deliberately avoids presenting competition performance as a publication result until the methodology, ablations, uncertainty evaluation and reproducibility package have been independently reviewed.

## Citation

See CITATION.cff. A formal paper citation will be added when a manuscript is publicly available.

## Competition

Developed for the MAEPiMS Challenge 2026 — Nigeria Influenza Forecasting Challenge.