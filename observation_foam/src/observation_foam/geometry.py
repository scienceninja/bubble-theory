"""Exact power-distance assignment; approximate sampled area balancing."""
import numpy as np

def power_assign(points, anchors, weights):
    points=np.asarray(points,dtype=float)
    anchors=np.asarray(anchors,dtype=float)
    weights=np.asarray(weights,dtype=float)
    if points.ndim!=2 or anchors.ndim!=2 or points.shape[1]!=anchors.shape[1]:
        raise ValueError("Mismatched dimensions")
    if not len(anchors) or weights.shape!=(len(anchors),):
        raise ValueError("One weight per anchor required")
    if not all(np.isfinite(a).all() for a in (points,anchors,weights)):
        raise ValueError("Nonfinite input")
    costs=np.einsum("ij,ij->i",anchors,anchors)[None,:]-2*points@anchors.T-weights[None,:]
    return np.argmin(costs,axis=1)

def sample_grid(resolution=120):
    if resolution<2: raise ValueError("Resolution must be >=2")
    c=(np.arange(resolution)+.5)/resolution
    x,y=np.meshgrid(c,c)
    return np.column_stack((x.ravel(),y.ravel()))

def cell_measure(labels,count):
    return np.bincount(np.asarray(labels,dtype=int).ravel(),minlength=count).astype(float)/len(labels)

def desired_area(inventory):
    inv=np.asarray(inventory,dtype=float)
    if inv.ndim!=1 or not np.isfinite(inv).all() or np.any(inv<=0):
        raise ValueError("Inventories must be positive and finite")
    return inv/inv.sum()

def balance_weights(anchors,inventory,resolution=120,iterations=120,step=.18):
    anchors=np.asarray(anchors,dtype=float)
    target=desired_area(inventory)
    if len(anchors)!=len(target): raise ValueError("Inventory/anchor mismatch")
    grid=sample_grid(resolution)
    weights=np.zeros(len(anchors))
    for _ in range(iterations):
        actual=cell_measure(power_assign(grid,anchors,weights),len(anchors))
        weights+=step*(target-actual)
        weights-=weights.mean()
    return weights,cell_measure(power_assign(grid,anchors,weights),len(anchors))

def boundary_equation(a,b,wa,wb):
    a,b=np.asarray(a,dtype=float),np.asarray(b,dtype=float)
    return 2*(b-a),float(b@b-a@a+wa-wb)
