# Pass 6 — Competition Submission Readiness

## Frozen model
ASEC-G (Adaptive Spatial Epidemic Clock with Gated Spatial Deformation).

The development evidence supports retaining this architecture: mean case MAE 332,019, RMSE 689,518, peak-week MAE 0.60 weeks, state case MAE 10,106, hospitalisation MAE 144.8, death MAE 14.3, and empirical central-80/90% coverage of 80.4%/88.8%.

These are rolling-origin development results over three synthetic seasons, not an independent hidden-test score.

## Required organizer input still missing
The supplied brief does not publish the official forecast CSV schema or hidden evaluation information set. Do not submit the provisional CSV as if it were official.

## Final execution
1. Obtain the official portal schema and designated forecast information set.
2. Point the pipeline at that information set only.
3. Run ASEC-G without future observations.
4. Convert weekly predictive distributions into required seasonal targets.
5. Run integrity checks.
6. Freeze the exact CSV, code, report PDF and GitHub commit used for submission.
