import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd


"""
# Suicide burn explorer
simplified model in vacuum, assume in vacuum, no aerodynamic drag, only thrust and gravity applied on vehicle. Thrust is fixed.

- $F_t$: Thrust
- $F_t - mg = ma$
- $F_t/m - g = a$  
"""

F = st.sidebar.number_input('Thrust (N)', value=10000)
mass = st.sidebar.number_input("Mass (KG)", value=1000)
g = st.sidebar.number_input("Gravitational acceleration (m/s^2)", value=9.8)

max_v = st.sidebar.number_input("Max vertical velocity (m/s^2)", value=300)

velocities = np.arange(max_v)
a = F/mass - g

# deacceleration burn time
suicide_b_time = velocities / a

# deacceleration burn distance
distances = velocities * suicide_b_time - 1/2 * a * suicide_b_time**2

# generate dataframe
df = pd.DataFrame({"velocity(m/s)": velocities, "burn_time(s)": suicide_b_time, "burn_distance(m)": distances})

# rendering
st.subheader(f"a = {a}")

"""
## suicide burn time
"""
fig = px.line(df, x = 'velocity(m/s)', y = 'burn_time(s)', title = 'burn time vs velocity')
st.plotly_chart(fig)

"""
## suicide burn distance
"""
fig = px.line(df, x = 'velocity(m/s)', y = 'burn_distance(m)', title = 'burn distance vs velocity')
st.plotly_chart(fig)

"""
## variable thrust, velocity at 300m/s
"""

velocity = 300

st.text(f"minimum thrust to maintain falling speed: {round(mass * g)} N")

variable_F = st.number_input('Max thrust (N)', value=2000)
Fs = np.arange(mass * g, variable_F)
accelerations = Fs/mass - g

burn_times = velocity / accelerations

burn_distances = velocity * burn_times - 1/2 * accelerations * burn_times**2
variable_thrust_dict = {"thrust(N)": Fs, "acceleration(m/s^2)": accelerations, "burn_time(s)": burn_times, "burn_distance(m)": burn_distances}

fig = px.line(variable_thrust_dict, x = 'acceleration(m/s^2)', y = 'burn_distance(m)', title = 'burn distance vs acceleration')
st.plotly_chart(fig)
