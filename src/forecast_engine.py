#!/usr/bin/env python3
"""ASEC-G provisional competition forecast engine."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

QLEVELS=[.05,.10,.25,.50,.75,.90,.95]
SEAS=['2023/2024','2024/2025','2025/2026']
ZONES=['NC','NE','NW','SE','SS','SW']

def smooth(x): return gaussian_filter1d(np.log1p(np.maximum(x,0)),1.25)
def clock(nat,seasons): return np.mean([smooth(nat[nat.season==s].sort_values('epi_week_of_season').cases.values) for s in seasons],0)
def phase(y,g):
    idx=np.arange(1,len(y)); ly=np.log1p(np.maximum(y,0)); best=(1e99,0,0)
    for sh in range(-6,7):
        hi=idx+sh
        if hi.min()<0 or hi.max()>=52: continue
        d=np.median(ly[idx]-g[hi]); e=np.mean((ly[idx]-g[hi]-d)**2)
        if e<best[0]: best=(e,sh,d)
    return best[1],best[2]
def feat(y,c):
    z=np.log1p(np.maximum(y[:c],0)); w=min(5,c)
    sl=np.polyfit(np.arange(w),z[-w:],1)[0]
    pr=z[-2*w:-w] if c>=2*w else z[:max(1,c-w)]
    slp=np.polyfit(np.arange(len(pr)),pr,1)[0] if len(pr)>1 else 0
    return [z[-1],sl,sl-slp,np.sum(y[:c])]
def asec_nat(nat,target,c,train):
    g=clock(nat,train); y=nat[nat.season==target].sort_values('epi_week_of_season').cases.values
    ly=np.log1p(y[:c]); idx=np.arange(1,c); ds=[]
    for sh in range(-6,7):
        hi=idx+sh
        if hi.min()>=0 and hi.max()<52: ds.append(np.median(ly[idx]-g[hi]))
    delta=float(np.median(ds)); return np.maximum(np.exp(g[c:]+delta)-1,0)
def fit_prop(st,states,train,target,c):
    X=[];Y=[]
    for s in train:
        for q in states:
            y=st[(st.season==s)&(st.state==q)].sort_values('epi_week_of_season').cases.values
            X.append(feat(y,c)); Y.append(np.clip((y[23:33].sum()+1)/(y[:24].sum()+1),0,2))
    m=make_pipeline(StandardScaler(),Ridge(alpha=2)).fit(X,Y); out=[]
    for q in states:
        y=st[(st.season==target)&(st.state==q)].sort_values('epi_week_of_season').cases.values
        out.append(np.clip(m.predict([feat(y,c)])[0],0,2))
    return np.asarray(out)
def components(nat,st,states,target,c,train):
    g=clock(nat,train); props=fit_prop(st,states,train,target,c); p0=asec_nat(nat,target,c,train); P=[]
    b=np.exp(-.5*((np.arange(52)-28)/5)**2)[c:]
    for j,q in enumerate(states):
        y=st[(st.season==target)&(st.state==q)].sort_values('epi_week_of_season').cases.values
        sh,d=phase(y[:c],g); idx=np.clip(np.rint(np.arange(c,52)+sh).astype(int),0,51)
        p=np.exp(g[idx]+d)-1; p*=np.exp((props[j]-.6)*b); P.append(p)
    P=np.asarray(P); ps=P.sum(0)
    obs=st[(st.season==target)&(st.epi_week_of_season<=c)].groupby('epi_week_of_season').cases.sum().values
    y=nat[nat.season==target].sort_values('epi_week_of_season').cases.values
    scale=np.median(y[1:c]/np.maximum(obs[1:],1)) if c>1 else 1.0
    return p0,P,ps*scale,props
def combine(p0,ps,lam=.4,start=16,week_offset=0):
    """Blend national and spatial components using absolute epi-week coordinates."""
    weeks=np.arange(len(p0))+week_offset
    gate=lam/(1+np.exp(-(weeks-start)/4))
    return np.maximum(np.exp((1-gate)*np.log1p(np.maximum(p0,0))+gate*np.log1p(np.maximum(ps,0)))-1,0)

def build(args):
    data=Path(args.data_dir)
    nat=pd.read_csv(data/'nigeria_flu_weekly_national.csv'); st=pd.read_csv(data/'nigeria_flu_weekly_by_state.csv'); meta=pd.read_csv(data/'nigeria_flu_state_metadata.csv').set_index('state')
    nat.season=nat.season.astype(str); st.season=st.season.astype(str); states=meta.index.tolist()
    if args.target_season not in SEAS: raise ValueError(f'target season must be one of {SEAS}')
    train=[s for s in SEAS if s!=args.target_season]
    p0,P,ps,props=components(nat,st,states,args.target_season,args.cutoff,train)
    pred_cases=combine(p0,ps,args.gate_lambda,args.gate_start,args.cutoff)
    gate=args.gate_lambda/(1+np.exp(-(np.arange(args.cutoff,52)-args.gate_start)/4))
    local=np.maximum(np.exp((1-gate[None,:])*np.log1p(np.maximum(p0[None,:],0))+gate[None,:]*np.log1p(np.maximum(P,0)))-1,0)
    weeks=nat[nat.season==args.target_season].sort_values('epi_week_of_season')
    rows=[]
    for i,w in enumerate(range(args.cutoff+1,53)):
        rows.append([args.target_season,weeks.iloc[w-1].week_start,w,'NATIONAL','national','cases',pred_cases[i]])
    for j,q in enumerate(states):
        for i,w in enumerate(range(args.cutoff+1,53)):
            rows.append([args.target_season,weeks.iloc[w-1].week_start,w,q,'state','cases',local[j,i]])
    for zone_name,zset in [('North',{'NC','NE','NW'}),('South',{'SE','SS','SW'})]:
        idx=[j for j,q in enumerate(states) if meta.loc[q,'zone'] in zset]
        for i,w in enumerate(range(args.cutoff+1,53)):
            rows.append([args.target_season,weeks.iloc[w-1].week_start,w,zone_name,'region','cases',local[idx,i].sum()])
    fc=pd.DataFrame(rows,columns=['season','week_start','epi_week_of_season','location','location_type','outcome','q50'])
    residuals=[]
    for val in train:
        tr=[s for s in train if s!=val]
        pp0,_,ppS,_=components(nat,st,states,val,args.cutoff,tr); pp=combine(pp0,ppS,args.gate_lambda,args.gate_start)
        yy=nat[nat.season==val].sort_values('epi_week_of_season').cases.values[args.cutoff:]
        residuals.extend(np.log1p(yy)-np.log1p(np.maximum(pp,0)))
    qs=np.quantile(np.asarray(residuals),QLEVELS); out=[]
    for r in fc.itertuples(index=False):
        center=np.log1p(max(r.q50,0)); vals=np.maximum(np.expm1(center+(qs-qs[3])*(1+args.uncertainty_inflation*max(0,(20-args.cutoff)/10))),0); out.append(vals)
    for k,q in enumerate(QLEVELS): fc[f'q{int(q*100):02d}']=np.asarray(out)[:,k]
    fc=fc.drop(columns=['q50']); fc['q50']=np.asarray(out)[:,3]
    cols=['season','week_start','epi_week_of_season','location','location_type','outcome']+[f'q{int(q*100):02d}' for q in QLEVELS]; fc=fc[cols]
    st2=st.merge(meta[['hc_access']],left_on='state',right_index=True); tr=st2[st2.season.isin(train)].copy(); tr['rH']=tr.hospitalizations/np.maximum(tr.cases,1); tr['rD']=tr.deaths/np.maximum(tr.cases,1)
    dfix=tr.loc[tr.cases>1000,'rD'].median(); tr=tr[tr.cases>1000]; X=[];Y=[]
    for _,r in tr.iterrows(): X.append([r.epi_week_of_season,r.hc_access]+[int(r.zone==z) for z in ZONES]); Y.append(np.log(max(r.rH,1e-7)))
    hm=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit(X,Y); sev_rows=[]; state_sev={}
    for j,q in enumerate(states):
        rr=st2[(st2.season==args.target_season)&(st2.state==q)].sort_values('epi_week_of_season')
        for outcome in ['hospitalizations','deaths']:
            vals=[]
            for _,r in rr[rr.epi_week_of_season>args.cutoff].iterrows():
                case=local[j,int(r.epi_week_of_season-args.cutoff-1)]
                v=case*dfix if outcome=='deaths' else case*np.exp(hm.predict([[r.epi_week_of_season,r.hc_access]+[int(r.zone==z) for z in ZONES]])[0])
                vals.append(max(float(v),0))
            state_sev[(q,outcome)]=np.asarray(vals)
            for i,w in enumerate(range(args.cutoff+1,53)): sev_rows.append([args.target_season,weeks.iloc[w-1].week_start,w,q,'state',outcome,vals[i]])
    for loc,zset in [('North',{'NC','NE','NW'}),('South',{'SE','SS','SW'}),('NATIONAL',set(ZONES))]:
        idx=[q for q in states if loc=='NATIONAL' or meta.loc[q,'zone'] in zset]
        for outcome in ['hospitalizations','deaths']:
            agg=np.sum([state_sev[(q,outcome)] for q in idx],axis=0); ltype='national' if loc=='NATIONAL' else 'region'
            for i,w in enumerate(range(args.cutoff+1,53)): sev_rows.append([args.target_season,weeks.iloc[w-1].week_start,w,loc,ltype,outcome,float(agg[i])])
    sev=pd.DataFrame(sev_rows,columns=['season','week_start','epi_week_of_season','location','location_type','outcome','point'])
    for outcome,spread in [('hospitalizations',.44),('deaths',.60)]:
        m=sev.outcome==outcome
        for q in QLEVELS: sev.loc[m,f'q{int(q*100):02d}']=sev.loc[m,'point']*np.exp((q-.5)*spread)
    sev=sev[['season','week_start','epi_week_of_season','location','location_type','outcome']+[f'q{int(q*100):02d}' for q in QLEVELS]]
    fc=pd.concat([fc,sev],ignore_index=True); outdir=Path(args.output_dir); outdir.mkdir(parents=True,exist_ok=True)
    fc.to_csv(outdir/f'forecast_PROVISIONAL_{args.target_season.replace("/","-")}_cutoff{args.cutoff}.csv',index=False)
    full_cases=np.r_[weeks.cases.values[:args.cutoff],pred_cases]; diagnostics={'season':args.target_season,'cutoff':args.cutoff,'predicted_peak_week':int(np.argmax(full_cases)+1),'predicted_peak_cases':float(full_cases.max()),'predicted_cumulative_cases':float(full_cases.sum()),'predicted_attack_rate_pct':float(100*full_cases.sum()/weeks.population.iloc[0])}
    for outcome in ['hospitalizations','deaths']:
        g=sev[(sev.location=='NATIONAL')&(sev.outcome==outcome)].sort_values('epi_week_of_season'); vals=np.r_[getattr(weeks,outcome).values[:args.cutoff],g.q50.values]
        diagnostics[f'predicted_cumulative_{outcome}']=float(vals.sum()); diagnostics[f'predicted_peak_week_{outcome}']=int(np.argmax(vals)+1); diagnostics[f'predicted_peak_{outcome}']=float(vals.max())
    pd.DataFrame([diagnostics]).to_csv(outdir/f'seasonal_diagnostics_{args.target_season.replace("/","-")}_cutoff{args.cutoff}.csv',index=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--data-dir',required=True); ap.add_argument('--target-season',required=True); ap.add_argument('--cutoff',type=int,required=True); ap.add_argument('--output-dir',required=True); ap.add_argument('--gate-lambda',type=float,default=.4); ap.add_argument('--gate-start',type=int,default=16); ap.add_argument('--uncertainty-inflation',type=float,default=.20); build(ap.parse_args())
