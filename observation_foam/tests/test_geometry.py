import numpy as np
import pytest
from observation_foam.geometry import power_assign,sample_grid,cell_measure,desired_area,balance_weights,boundary_equation

def test_equal_cells():
    labels=power_assign(sample_grid(120),[[.25,.5],[.75,.5]],[0,0])
    assert np.allclose(cell_measure(labels,2),[.5,.5])

def test_flat_unweighted_boundary():
    n,c=boundary_equation([.25,.5],[.75,.5],0,0)
    assert np.isclose(np.dot(n,[.5,.2]),c)
    assert np.isclose(np.dot(n,[.5,.9]),c)

def test_weighted_boundary_still_flat():
    n,c=boundary_equation([.25,.5],[.75,.5],.2,0)
    assert np.isclose(c/n[0],.7)

def test_weight_increases_area():
    grid=sample_grid(100)
    anchors=[[.25,.5],[.75,.5]]
    before=cell_measure(power_assign(grid,anchors,[0,0]),2)
    after=cell_measure(power_assign(grid,anchors,[.15,0]),2)
    assert after[0]>before[0]

def test_inventory_normalization():
    assert np.allclose(desired_area([1,2,3]),[1/6,2/6,3/6])

def test_weight_balancing():
    anchors=np.array([[.2,.25],[.75,.25],[.5,.8]])
    target=desired_area([1,2,4])
    grid=sample_grid(100)
    initial=cell_measure(power_assign(grid,anchors,[0,0,0]),3)
    w,actual=balance_weights(anchors,[1,2,4],100,160,.15)
    assert abs(actual-target).sum()<abs(initial-target).sum()
    assert max(abs(actual-target))<.025
    assert abs(w.mean())<1e-12

def test_determinism():
    anchors=[[.2,.25],[.75,.25],[.5,.8]]
    a=balance_weights(anchors,[1,2,3],50)
    b=balance_weights(anchors,[1,2,3],50)
    assert all(np.array_equal(x,y) for x,y in zip(a,b))

def test_invalid_input():
    with pytest.raises(ValueError): desired_area([1,0])
    with pytest.raises(ValueError): power_assign([[.2,.3]],[[.2,.3]],[float("nan")])
