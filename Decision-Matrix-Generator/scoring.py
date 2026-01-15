import pandas as pd
import numpy as np

def compute_scores(df_options, criteria, weights, safety_criterion="Safety", safety_threshold=0.6):
    df = df_options.copy()

    # Normalise weights
    w = np.array(weights)
    w = w / np.sum(w) if np.sum(w) != 0 else np.ones(len(w)) / len(w)

    # Normalise scores per criterion (0–1)
    norm_scores = []
    for c in criteria:
        col = df[c].values.astype(float)
        if col.max() != col.min():
            norm = (col - col.min()) / (col.max() - col.min())
        else:
            norm = np.ones(len(col))
        norm_scores.append(norm)

    norm_matrix = np.vstack(norm_scores).T

    # Weighted score
    df["Score"] = norm_matrix.dot(w)

    # Safety gate
    if safety_criterion in criteria:
        safety_norm = norm_matrix[:, criteria.index(safety_criterion)]
        df["Safety_Pass"] = safety_norm >= safety_threshold
        df.loc[~df["Safety_Pass"], "Score"] = 0  # fail-safe override
    else:
        df["Safety_Pass"] = True

    # Rank results
    df = df.sort_values("Score", ascending=False)

    return df
