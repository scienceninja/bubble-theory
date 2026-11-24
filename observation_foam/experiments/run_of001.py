"""Deterministic exploratory check of inventory-to-area fitting."""
import json
from pathlib import Path
import numpy as np
from observation_foam.geometry import sample_grid,power_assign,cell_measure,desired_area,balance_weights

anchors=np.array([[.18,.21],[.67,.16],[.82,.69],[.38,.75],[.21,.49]])
inventory=np.array([1,4,2,3,2])
grid=sample_grid(150)
before=cell_measure(power_assign(grid,anchors,np.zeros(5)),5)
weights,after=balance_weights(anchors,inventory,150,180,.15)
target=desired_area(inventory)
result={"status":"exploratory geometry only",
"anchors":anchors.tolist(),"inventory":inventory.tolist(),
"target_area":target.tolist(),"unweighted_area":before.tolist(),
"balanced_area":after.tolist(),"weights":weights.tolist(),
"unweighted_l1_error":float(abs(before-target).sum()),
"balanced_l1_error":float(abs(after-target).sum()),
"flat_interfaces_by_construction":True}
print(json.dumps(result,indent=2))
