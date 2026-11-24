import numpy as np
import pytest
from bubble_theory.engine import SimulationConfig, simulate, ring_neighbors, initial_conditions, drift

def test_ring_is_degree_eight_symmetric():
    nbr = ring_neighbors(128, 4)
    assert nbr.shape == (128, 8)
    assert all(i not in nbr[i] for i in range(128))
    assert all(i in nbr[j] for i in range(128) for j in nbr[i])

def test_reproducible():
    cfg = SimulationConfig(n=16, radius=2, dt=.02, duration=2)
    assert np.array_equal(simulate(42, 2, .2, cfg), simulate(42, 2, .2, cfg))
    assert not np.array_equal(simulate(42, 2, .2, cfg), simulate(43, 2, .2, cfg))

def test_uncoupled_exact_deterministic_solution():
    cfg = SimulationConfig(n=16, radius=2, dt=.02, duration=2)
    omega, theta = initial_conditions(7, 16)
    path = simulate(7, 0, 0, cfg)
    expected = np.mod(theta[None, :] + np.arange(len(path))[:, None] * cfg.dt * omega[None, :], 2 * np.pi)
    assert np.allclose(np.exp(1j * path), np.exp(1j * expected), atol=1e-12)

def test_identical_synchronized_oscillators_stay_synchronized_without_noise():
    cfg = SimulationConfig(n=16, radius=2, dt=.02, duration=1)
    path = simulate(0, 4, 0, cfg, omega=np.ones(16), theta0=np.ones(16) * 1.23)
    assert np.max(np.abs(np.exp(1j * path) - np.exp(1j * path[:, :1]))) < 1e-12

def test_uniform_phase_shift_invariant_drift():
    n = 16
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    omega = np.arange(n) * .01
    neighbors = ring_neighbors(n, 2)
    assert np.allclose(drift(theta, omega, 2, neighbors), drift(theta + 1.2, omega, 2, neighbors))

def test_unsupported_config_rejected():
    with pytest.raises(ValueError):
        SimulationConfig(n=8, radius=4)

def test_independent_noise_disrupts_perfect_synchrony():
    cfg = SimulationConfig(n=16, radius=2, dt=.02, duration=1)
    base = dict(omega=np.zeros(16), theta0=np.ones(16))
    clean = simulate(10, 2, 0, cfg, **base)
    noisy = simulate(10, 2, 1, cfg, **base)
    assert np.max(np.abs(clean - clean[:, :1])) < 1e-12
    assert np.std(noisy[-1]) > .01

def test_deterministic_step_halving_converges():
    omega = np.linspace(-.3, .3, 16)
    theta = np.linspace(0, 1.2, 16)
    coarse = simulate(3, 1.5, 0, SimulationConfig(n=16, radius=2, dt=.04, duration=2), omega=omega, theta0=theta)
    medium = simulate(3, 1.5, 0, SimulationConfig(n=16, radius=2, dt=.02, duration=2), omega=omega, theta0=theta)
    fine = simulate(3, 1.5, 0, SimulationConfig(n=16, radius=2, dt=.01, duration=2), omega=omega, theta0=theta)
    e1 = np.linalg.norm(np.exp(1j * coarse[-1]) - np.exp(1j * medium[-1]))
    e2 = np.linalg.norm(np.exp(1j * medium[-1]) - np.exp(1j * fine[-1]))
    assert e2 < e1
