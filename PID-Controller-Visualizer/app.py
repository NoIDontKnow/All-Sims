import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from controller import PID
from plant import FirstOrderPlant

st.title("PID Controller Visualizer")

kp = st.sidebar.slider("Kp", 0.0, 10.0, 1.0)
ki = st.sidebar.slider("Ki", 0.0, 5.0, 0.1)
kd = st.sidebar.slider("Kd", 0.0, 5.0, 0.0)
tau = st.sidebar.slider("Plant time constant (tau)", 0.1, 10.0, 1.0)
gain = st.sidebar.slider("Plant gain", 0.1, 5.0, 1.0)
dt = st.sidebar.number_input("dt", 0.01, 1.0, 0.05)
steps = st.sidebar.number_input("Simulation steps", 50, 2000, 400)
setpoint = st.sidebar.number_input("Setpoint", -10.0, 10.0, 1.0)

pid = PID(kp, ki, kd, dt, integrator_limit=1000.0)
plant = FirstOrderPlant(time_constant=tau, gain=gain, dt=dt)

u_history = []; y_history = []; e_history = []; t_history=[]
for i in range(int(steps)):
    t = i*dt
    y = plant.state
    u, e = pid.step(setpoint, y)
    plant.step(u)
    u_history.append(u); y_history.append(plant.state); e_history.append(e); t_history.append(t)

fig, ax = plt.subplots(2, 1, figsize=(8,6))
ax[0].plot(t_history, y_history, label="Output")
ax[0].plot(t_history, [setpoint]*len(t_history), "--", label="Setpoint")
ax[0].legend(); ax[0].set_ylabel("Output")
ax[1].plot(t_history, u_history, label="Control signal")
ax[1].plot(t_history, e_history, label="Error")
ax[1].legend(); ax[1].set_ylabel("Control / Error")
ax[1].set_xlabel("Time (s)")
st.pyplot(fig)

st.write("Tweak Kp/Ki/Kd and observe overshoot, settling time, and steady-state error.")
