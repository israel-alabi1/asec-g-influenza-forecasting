# Validation protocol

## Design
Target season is held out. For each target season, forecasts are generated at weeks 10, 12, 15, 18 and 20. Only the observed prefix of the target season is available to the forecasting procedure.

## Primary metrics
- MAE
- RMSE
- peak-week absolute error
- peak-incidence relative error
- full-season cumulative-case relative error

## Probabilistic metrics
- central 80% coverage
- central 90% coverage
- interval score/WIS-like interval score

## Spatial metrics
State-week MAE is calculated over the forecast horizon. Zone summaries are reported separately.

## Caveat
Only three seasons are available. Hyperparameter tuning and validation are necessarily limited. Rolling-origin scores should be described as development evidence, not as an untouched leaderboard score.
