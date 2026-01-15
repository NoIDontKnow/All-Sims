import streamlit as st
import pandas as pd
import numpy as np
from allocator import proportional_allocation, constrained_allocation

st.title("Resource Allocation Tool")

n = st.number_input("Number of regions", 1, 20, 5)
regions = []
weights = []
mins = []
maxs = []
for i in range(int(n)):
    name = st.text_input(f"Region {i} name", f"R{i+1}", key=f"name{i}")
    w = st.number_input(f"Weight {i}", 0.0, 100.0, 1.0, key=f"w{i}")
    mn = st.number_input(f"Min req {i}", 0.0, 1e6, 0.0, key=f"mn{i}")
    mx = st.number_input(f"Max cap {i}", 0.0, 1e9, 1e6, key=f"mx{i}")
    regions.append(name); weights.append(w); mins.append(mn); maxs.append(mx)

total = st.number_input("Total resource to allocate", 0.0, 1e9, 1000.0)

if st.button("Allocate proportionally"):
    alloc = proportional_allocation(total, weights)
    df = pd.DataFrame({"Region": regions, "Weight": weights, "Allocation": alloc})
    st.write(df)
    st.download_button("Export CSV", df.to_csv(index=False), "alloc.csv")

if st.button("Allocate with mins/maxs"):
    alloc = constrained_allocation(total, mins, maxs, weights)
    df = pd.DataFrame({"Region": regions, "Min": mins, "Max": maxs, "Allocation": alloc})
    st.write(df)
    st.download_button("Export CSV", df.to_csv(index=False), "alloc_constrained.csv")
