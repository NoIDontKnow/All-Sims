import streamlit as st
import pandas as pd
from scoring import compute_scores

st.title("Decision Matrix Generator")

st.sidebar.header("Config")
criteria_input = st.sidebar.text_area("Criteria (comma-separated)", "Cost,Time,Impact")
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
weights = []
for c in criteria:
    weights.append(st.sidebar.slider(f"Weight: {c}", 0.0, 10.0, 1.0))

st.header("Options")
num = st.number_input("Number of options", 1, 20, 3)
scores_data = {c: [] for c in criteria}
names = []
for i in range(int(num)):
    name = st.text_input(f"Option {i+1} name", f"Option {i+1}", key=f"name{i}")
    names.append(name)
    for c in criteria:
        val = st.number_input(f"Score for {name} on {c}", 0.0, 10.0, 5.0, key=f"{name}-{c}")
        scores_data[c].append(val)

df = pd.DataFrame(scores_data)
df.insert(0, "Option", names)
if st.button("Compute rankings"):
    result = compute_scores(df, criteria, weights)
    st.write(result)
    st.download_button("Export CSV", result.to_csv(index=False), "decision_results.csv")
