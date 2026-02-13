import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("Electrical Fault Detection Simulator")
st.markdown("""
This interactive tool simulates electrical sensor data and helps users practice **fault detection** in power systems.
Use the sliders to set thresholds and observe how faults are detected in real-time.
""")

# Generate simulated data
@st.cache_data
def generate_data():
    np.random.seed(42)
    time = np.arange(0, 100, 0.1)
    voltage = 230 + np.random.normal(0, 2, len(time))
    current = 10 + np.random.normal(0, 0.5, len(time))

    # Introduce faults
    voltage[500:550] += 50  # Voltage spike
    current[800:850] -= 5   # Current drop

    df = pd.DataFrame({
        'Time': time,
        'Voltage (V)': voltage,
        'Current (A)': current
    })
    df.to_csv('data.csv', index=False)
    return df

# Load data
data = generate_data()

# Plot data
st.subheader("Simulated Sensor Data")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data['Time'], data['Voltage (V)'], label='Voltage', color='blue')
ax.plot(data['Time'], data['Current (A)'], label='Current', color='orange')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Value')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# User inputs for thresholds
st.sidebar.header("Fault Detection Settings")
voltage_threshold = st.sidebar.slider("Voltage Threshold (V)", 200, 300, 250)
current_threshold_low = st.sidebar.slider("Current Lower Threshold (A)", 5, 15, 8)
current_threshold_high = st.sidebar.slider("Current Upper Threshold (A)", 5, 15, 12)

# Detect faults
voltage_faults = data[data['Voltage (V)'] > voltage_threshold]
current_faults = data[(data['Current (A)'] < current_threshold_low) | (data['Current (A)'] > current_threshold_high)]

# Display results
st.subheader("Fault Detection Results")
st.write(f"**Voltage Faults Detected:** {len(voltage_faults)}")
st.write(f"**Current Faults Detected:** {len(current_faults)}")

if len(voltage_faults) > 0:
    st.write("### Voltage Faults")
    st.dataframe(voltage_faults.style.highlight_max(axis=0))
if len(current_faults) > 0:
    st.write("### Current Faults")
    st.dataframe(current_faults.style.highlight_max(axis=0))

# Download data
st.download_button(
    label="Download Simulated Data",
    data=data.to_csv(index=False).encode('utf-8'),
    file_name='electrical_sensor_data.csv',
    mime='text/csv',
)

# Learning tips
st.sidebar.markdown("---
**Learning Tips:**
- Adjust thresholds to see how sensitivity affects fault detection.
- Try adding more faults to the data and see if you can detect them!
- Think about how you would apply this to real-world systems.")
