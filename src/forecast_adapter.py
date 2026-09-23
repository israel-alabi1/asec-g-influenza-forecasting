"""Provisional MAEPiMS forecast-schema adapter."""
from pathlib import Path
import pandas as pd
QCOLS=['q05','q10','q25','q50','q75','q90','q95']
def validate_quantiles(df):
    if not all(c in df.columns for c in QCOLS): raise ValueError('Missing quantile columns')
    x=df[QCOLS].to_numpy()
    if (x<0).any(): raise ValueError('Negative forecast')
    if not (x[:,1:]>=x[:,:-1]).all(): raise ValueError('Non-monotone quantiles')
def write(df,path):
    validate_quantiles(df); Path(path).parent.mkdir(parents=True,exist_ok=True); df.to_csv(path,index=False)
