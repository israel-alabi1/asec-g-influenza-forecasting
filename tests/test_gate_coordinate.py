"""Regression tests for the ASEC-G gate coordinate.

Run with:
    python tests/test_gate_coordinate.py
"""
import importlib.util
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("forecast_engine",ROOT/"src"/"forecast_engine.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

p0=np.ones(32)*100.0
ps=np.ones(32)*200.0

# With cutoff=20 and gate_start=16, the first forecast week is already
# beyond the gate midpoint. The gate must therefore exceed lambda/2.
out=m.combine(p0,ps,lam=.4,start=16,week_offset=20)

# At absolute week 20, lambda = .4/(1+exp(-(20-16)/4)).
expected=.4/(1+np.exp(-1))
assert expected > .25
# Recover the implied blend from log1p values.
implied=(np.log1p(out[0])-np.log1p(100.0))/(np.log1p(200.0)-np.log1p(100.0))
assert np.isclose(implied,expected,rtol=1e-10,atol=1e-10)

# The gate must be increasing over the forecast horizon.
assert np.all(np.diff([
    .4/(1+np.exp(-((w-16)/4))) for w in range(20,52)
]) > 0)

print("PASS: absolute-week gate coordinate regression test")
