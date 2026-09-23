# Adaptive Spatial Epidemic Clock with Gated Spatial Deformation (ASEC-G)

## Model

```
log(1 + Y[s,t]) = G(t - tau[s]) + b[s] + A[s] B2(t) + epsilon[s,t]
```

- `G`: latent national epidemic clock obtained from smoothed national log-cases.
- `tau[s]`: state phase estimated from observed state-vs-clock alignment.
- `A[s]`: secondary-wave propensity from observed level, recent slope, acceleration and cumulative activity.
- `B2`: smooth late-season secondary activation basis.
- noise: log-scale multiplicative uncertainty.

## Validation
Target season is held out. Forecast origins are weeks 10, 12, 15, 18 and 20. Only the two non-target seasons plus the observed target prefix are used.

## Probabilistic layer
Quantiles: 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95.
Regime ambiguity is widened near the primary-to-secondary transition.
