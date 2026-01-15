import numpy as np
from scipy.ndimage import gaussian_filter

def generate_base_grid(size=(100,100), seed=None):
    rng = np.random.RandomState(seed)
    base = rng.rand(*size)
    for _ in range(5):
        x = rng.randint(0, size[0])
        y = rng.randint(0, size[1])
        base += np.exp(-((np.indices(size)[0]-x)**2 + (np.indices(size)[1]-y)**2)/(2*(size[0]*0.05)**2))
    base = gaussian_filter(base, sigma=size[0]*0.02)
    base = (base - base.min())/(base.max()-base.min()+1e-9)
    return base

def simulate_growth(base, steps=10, growth_rate=0.05, accessibility=None):
    grid = base.copy()
    for _ in range(steps):
        influence = gaussian_filter(grid, sigma=1.0)
        prob = growth_rate * (influence + 0.2)
        grow = (np.random.rand(*grid.shape) < prob)
        grid = np.clip(grid + grow*0.05, 0, 1)
    return grid
