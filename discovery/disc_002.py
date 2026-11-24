"""DISC-002: exploratory domain phase-kick experiment.

Runs 12 matched trios: sham, within-domain phase kick and outside-domain kick.
This is NOT BT-EXP-001. Use: python discovery/disc_002.py
"""
import csv
import json
from pathlib import Path
import numpy as np
from bubble_theory.engine import SimulationConfig, simulate, initial_conditions, increments, drift, ring_neighbors
from bubble_theory.detection import candidates, edges_for_ring, scores

N=128
DT=.02
T0=7500
T1=10000
SEEDS=(0,1,2)
COUPLINGS=(1.,2.)
NOISES=(0.,.2)

def continuation(start, omega, innovations, neighbors, coupling, noise):
    state=start.copy()
    output=np.empty((T1-T0,N),dtype=np.float64)
    for j in range(T1-T0):
        state=(state+DT*drift(state,omega,coupling,neighbors)+noise*np.sqrt(DT)*innovations[T0+j])%(2*np.pi)
        output[j]=state
    return output

def run(output="discovery/DISC-002-results"):
    out=Path(output)
    out.mkdir(parents=True,exist_ok=True)
    edges=edges_for_ring(N,4)
    neighbors=ring_neighbors(N,4)
    cfg=SimulationConfig()
    rows=[]
    for seed in SEEDS:
      omega,initial=initial_conditions(seed,N)
      innovations=increments(seed,N,T1)
      for sigma in NOISES:
        for coupling in COUPLINGS:
          trajectory=simulate(seed,coupling,sigma,cfg)
          groups=candidates(trajectory[5000:7500],edges)
          if not groups:
              rows.append(dict(seed=seed,K=coupling,sigma=sigma,condition="no_candidate"))
              continue
          domain=sorted(groups,key=lambda g:(-len(g),g))[0]
          rng=np.random.default_rng(np.random.SeedSequence([seed,int(coupling*10),int(sigma*10),202]))
          count=max(1,int(np.ceil(len(domain)/2)))
          within=np.sort(rng.choice(domain,count,replace=False))
          outside=np.sort(rng.choice([i for i in range(N) if i not in domain],count,replace=False))
          for condition,indices in (("sham",[]),("inside_kick",within),("outside_kick",outside)):
            start=trajectory[T0].copy()
            if len(indices):
                start[indices]=(start[indices]+np.pi)%(2*np.pi)
            path=continuation(start,omega,innovations,neighbors,coupling,sigma)
            early=scores(path[:500],edges,domain)
            late=scores(path[2000:2500],edges,domain)
            rows.append(dict(seed=seed,K=coupling,sigma=sigma,condition=condition,
                domain_size=len(domain),kick_size=count,domain_nodes=list(domain),
                kick_nodes=list(map(int,indices)),early_internal=early[0],
                early_distinction=early[1],late_internal=late[0],
                late_distinction=late[1]))
    (out/"raw.json").write_text(json.dumps(rows,indent=2)+"\n")
    flat=[{k:(json.dumps(v) if isinstance(v,list) else v) for k,v in row.items()} for row in rows]
    with (out/"raw.csv").open("w",newline="") as f:
        fields=sorted(set().union(*(r.keys() for r in flat)))
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(flat)
    for condition in ("sham","inside_kick","outside_kick"):
        cases=[r for r in rows if r["condition"]==condition]
        print(condition,"n",len(cases),
              "early distinction",np.mean([r["early_distinction"] for r in cases]),
              "late distinction",np.mean([r["late_distinction"] for r in cases]))

if __name__=="__main__":
    run()
