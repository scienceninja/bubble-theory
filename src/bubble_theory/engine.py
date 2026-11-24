"""Noisy local Kuramoto dynamics with no bubble-dependent rules."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class SimulationConfig:
    n: int = 128
    radius: int = 4
    dt: float = 0.02
    duration: float = 250.0

    def __post_init__(self):
        if self.radius < 1 or self.n < 2 * self.radius + 2:
            raise ValueError("Invalid ring dimensions")
        if self.dt <= 0 or self.duration <= 0:
            raise ValueError("Time values must be positive")
        if abs(self.duration / self.dt - round(self.duration / self.dt)) > 1e-9:
            raise ValueError("Duration must be an integer number of steps")

def ring_neighbors(n: int, radius: int):
    if radius < 1 or n < 2 * radius + 2:
        raise ValueError("Invalid ring dimensions")
    offsets = np.array(list(range(-radius, 0)) + list(range(1, radius + 1)))
    return (np.arange(n)[:, None] + offsets[None, :]) % n

def initial_conditions(seed: int, n: int):
    rng = np.random.default_rng(np.random.SeedSequence([seed, 0]))
    return rng.normal(size=n), rng.uniform(0, 2 * np.pi, size=n)

def increments(seed: int, n: int, steps: int):
    rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
    return rng.standard_normal((steps, n))

def drift(theta, omega, coupling, neighbors):
    return omega + coupling * np.sin(theta[neighbors] - theta[:, None]).mean(axis=1)

def simulate(seed: int, coupling: float, noise: float, config: SimulationConfig = SimulationConfig(),
             *, omega=None, theta0=None, standard_normals=None):
    """Euler-Maruyama trajectory; t=0,dt,...,duration; float64."""
    if coupling < 0 or noise < 0:
        raise ValueError("Coupling and noise must be nonnegative")
    n, dt = config.n, config.dt
    steps = round(config.duration / dt)
    if omega is None or theta0 is None:
        w, p = initial_conditions(seed, n)
        omega = w if omega is None else np.asarray(omega)
        theta0 = p if theta0 is None else np.asarray(theta0)
    omega, theta0 = np.asarray(omega, dtype=np.float64), np.asarray(theta0, dtype=np.float64)
    if omega.shape != (n,) or theta0.shape != (n,):
        raise ValueError("Initial data shape mismatch")
    if standard_normals is None:
        standard_normals = increments(seed, n, steps)
    if standard_normals.shape != (steps, n):
        raise ValueError("Innovations shape mismatch")
    neighbors = ring_neighbors(n, config.radius)
    path = np.empty((steps + 1, n), dtype=np.float64)
    theta = np.mod(theta0.copy(), 2 * np.pi)
    path[0] = theta
    sqrt_dt = np.sqrt(dt)
    for k in range(steps):
        theta += dt * drift(theta, omega, coupling, neighbors) + noise * sqrt_dt * standard_normals[k]
        theta %= 2 * np.pi
        path[k + 1] = theta
    return path
