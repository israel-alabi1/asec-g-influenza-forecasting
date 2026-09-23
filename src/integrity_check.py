import argparse, pandas as pd, numpy as np
Q=['q05','q10','q25','q50','q75','q90','q95']; K=['season','week_start','epi_week_of_season','location','location_type','outcome']
ap=argparse.ArgumentParser(); ap.add_argument('csv'); a=ap.parse_args()
df=pd.read_csv(a.csv); errs=[]
for c in K+Q:
    if c not in df.columns: errs.append(f'missing:{c}')
if not errs:
    if df[K].isna().any().any() or df[Q].isna().any().any(): errs.append('missing values')
    if (df[Q]<0).any().any(): errs.append('negative forecast')
    if not np.all(np.diff(df[Q].to_numpy(),axis=1)>=-1e-9): errs.append('non-monotone quantiles')
    if df.duplicated(K).any(): errs.append('duplicate keys')
    if not df.epi_week_of_season.between(1,52).all(): errs.append('invalid epi week')
print(f'rows={len(df):,}; locations={df.location.nunique()}; outcomes={df.outcome.nunique()}')
if errs: print('FAIL'); print('\n'.join(errs)); raise SystemExit(1)
print('PASS: structural integrity checks passed')
