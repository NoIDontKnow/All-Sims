import numpy as np
from math import log10
from scipy.optimize import fsolve

def pH_from_H(H):
    return -np.log10(H)

def ph_of_strong_acid(c):
    # [H+] = c
    return -np.log10(c)

def titration_strong_acid_vs_strong_base(Ca, Va, Cb, Vb_steps=500):
    # Add base incrementally; compute [H+]
    volumes = np.linspace(0, Vb_steps, Vb_steps)
    H = []
    for vb in volumes:
        # convert mL to L consistently if needed; here we treat volumes in same units
        ma = Ca * Va
        mb = Cb * vb
        net = ma - mb
        if net > 0:
            # excess acid: [H+] = net / total volume
            H.append(net / (Va + vb))
        elif net < 0:
            # excess base: [OH-] = (-net) / total volume
            OH = (-net) / (Va + vb)
            H.append(1e-14 / OH)
        else:
            # equivalence: neutralization -> water solution (approx)
            H.append(1e-7)
    phs = -np.log10(np.array(H))
    return volumes, phs

# Weak acid titration (simplified): Henderson-Hasselbalch for buffer region.
def titration_weak_acid(Ca, Va, Ka, Cb, Vb_steps=500):
    vb = np.linspace(0, Vb_steps, Vb_steps)
    phs = []
    for v in vb:
        ma = Ca * Va
        mb = Cb * v
        A = max(ma - mb, 0.0)
        B = max(mb, 0.0)
        Vtot = Va + v
        if A > 0 and B > 0:
            pKa = -np.log10(Ka)
            ph = pKa + np.log10(B / A)
        elif A > 0 and B == 0:
            C = Ca * Va / Vtot
            # quadratic: [H+]^2 + Ka*[H+] - Ka*C = 0
            H = ( -Ka + np.sqrt(Ka**2 + 4*Ka*C) )/2
            ph = -np.log10(H)
        else:
            Cb_equiv = (mb - ma) / Vtot
            Kb = 1e-14/Ka
            OH = ( -Kb + np.sqrt(Kb**2 + 4*Kb*Cb_equiv) )/2
            H = 1e-14 / OH
            ph = -np.log10(H)
        phs.append(ph)
    return vb, np.array(phs)
