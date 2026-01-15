import numpy as np
import pandas as pd

def proportional_allocation(total, weights):
    w = np.array(weights, dtype=float)
    if w.sum() == 0:
        return np.zeros_like(w)
    alloc = (w / w.sum()) * total
    return alloc

def constrained_allocation(total, mins, maxs, weights):
    n = len(weights)
    alloc = np.array(mins, dtype=float)
    rem_total = total - alloc.sum()
    rem_caps = np.array(maxs, dtype=float) - alloc
    if rem_total <= 0:
        return np.minimum(alloc, maxs)
    w = np.array(weights, dtype=float)
    w[rem_caps<=0] = 0
    if w.sum() == 0:
        fill = np.minimum(rem_caps, rem_total / max(1, (rem_caps>0).sum()))
        return alloc + fill
    prop = (w / w.sum()) * rem_total
    prop = np.minimum(prop, rem_caps)
    alloc += prop
    leftover = total - alloc.sum()
    if leftover > 1e-6:
        for i in np.argsort(-w):
            take = min(leftover, rem_caps[i] - prop[i])
            if take > 0:
                alloc[i] += take
                leftover -= take
            if leftover <= 1e-6:
                break
    return alloc
