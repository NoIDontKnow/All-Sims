import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from chemistry import titration_strong_acid_vs_strong_base, titration_weak_acid

st.set_page_config(layout="wide", page_title="Biochem Lab Simulator")

st.title("Biochem Lab Simulator")

tab = st.radio("Mode", ["Titration (strong/strong)", "Titration (weak/strong)", "1D Diffusion demo"])

if tab.startswith("Titration"):
    if "strong/strong" in tab:
        st.header("Strong acid titration with strong base")
        Ca = st.number_input("Acid concentration (M)", 0.001, 1.0, 0.1, step=0.001)
        Va = st.number_input("Acid volume (mL)", 1.0, 50.0, 25.0, step=0.1)
        Cb = st.number_input("Base concentration (M)", 0.001, 1.0, 0.1, step=0.001)
        Vb_max = st.number_input("Max added base volume (mL)", 10.0, 200.0, 100.0, step=1.0)
        steps = int(st.slider("Curve resolution (steps)", 100, 2000, 500))
        vb, phs = titration_strong_acid_vs_strong_base(Ca, Va, Cb, Vb_steps=steps)
        fig, ax = plt.subplots()
        ax.plot(vb, phs)
        ax.set_xlabel("Added base volume (mL)")
        ax.set_ylabel("pH")
        st.pyplot(fig)
    else:
        st.header("Weak acid titration with strong base (approx)")
        Ca = st.number_input("Weak acid concentration (M)", 0.001, 1.0, 0.1, step=0.001)
        Va = st.number_input("Acid volume (mL)", 1.0, 50.0, 25.0, step=0.1)
        Ka = st.number_input("Ka (e.g., 1e-5)", 1e-10, 1e-1, 1e-5, format="%.1e", step=1e-6)
        Cb = st.number_input("Base concentration (M)", 0.001, 1.0, 0.1, step=0.001)
        steps = int(st.slider("Curve resolution (steps)", 100, 2000, 500))
        vb, phs = titration_weak_acid(Ca, Va, Ka, Cb, Vb_steps=steps)
        fig, ax = plt.subplots()
        ax.plot(vb, phs)
        ax.set_xlabel("Added base volume (mL)")
        ax.set_ylabel("pH")
        st.pyplot(fig)

else:
    st.header("1D Diffusion demo (explicit finite difference)")
    length = st.slider("Grid size (cells)", 50, 500, 150)
    dt = st.slider("Time step (dt)", 0.01, 1.0, 0.2)
    diff = st.slider("Diffusion coefficient", 0.01, 5.0, 0.5)
    steps = st.slider("Simulation steps", 10, 200, 60)
    grid = np.zeros(length)
    grid[length//2] = 1.0
    frames = []
    for _ in range(steps):
        nextg = np.copy(grid)
        for i in range(1, length-1):
            nextg[i] = grid[i] + diff*dt*(grid[i-1]-2*grid[i]+grid[i+1])
        grid = nextg
        frames.append(grid.copy())
    fig, ax = plt.subplots()
    ax.plot(frames[-1])
    ax.set_xlabel("Cell")
    ax.set_ylabel("Concentration")
    st.pyplot(fig)
    st.write("You can export frames to CSV for animation in external tools.")
