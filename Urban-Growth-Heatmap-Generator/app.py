import streamlit as st
import matplotlib.pyplot as plt
from generator import generate_base_grid, simulate_growth

st.title("Urban Growth Heatmap Generator")

size = st.slider("Grid size (square)", 50, 300, 100)
seed = st.number_input("Random seed (int)", 0, 9999999, 42)
steps = st.slider("Simulation steps", 1, 200, 20)
growth_rate = st.slider("Growth rate", 0.0, 0.5, 0.05)

base = generate_base_grid(size=(size,size), seed=seed)
st.subheader("Base attractiveness")
fig, ax = plt.subplots()
ax.imshow(base, cmap='hot')
ax.axis('off')
st.pyplot(fig)

grid = simulate_growth(base, steps=steps, growth_rate=growth_rate)
st.subheader("After growth")
fig2, ax2 = plt.subplots()
ax2.imshow(grid, cmap='hot')
ax2.axis('off')
st.pyplot(fig2)

st.write("Export arrays as CSV for GIS or further analysis.")
