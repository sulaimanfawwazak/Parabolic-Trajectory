import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import charminal as ch

plt.style.use('fivethirtyeight')
mpl.rcParams['font.size'] = 10
mpl.rcParams['lines.linewidth'] = 3

########################## CONSTANTS ##########################
###############################################################

g = 9.807

########################## FUNCTIONS ##########################
###############################################################

# Calculate the max range
def calc_range(v_0, theta, g=9.807):
  return v_0**2 * np.sin(2*np.radians(theta)) / g

# Calculate the flight time
def calc_t_flight(v_0, theta, g=9.807):
  return 2 * v_0 * np.sin(np.radians(theta)) / g

# Calculate the max height
def calc_h_max(v_0, theta, g=9.807):
  return (v_0 * np.sin(np.radians(theta)))**2 / (2*g)

# Calculate the time of max height
def calc_t_h_max(v_0, theta, g=9.807):
  return v_0 * np.sin(np.radians(theta)) / g

# Calculate the x at t
def calc_x_t(t, v_0, theta):
  return v_0 * np.cos(np.radians(theta)) * t

# Calculate y at t
def calc_y_t(t, v_0, theta, g=9.807):
  return v_0 * np.sin(np.radians(theta)) * t - 1/2 * g * t**2

########################## INPUTS ##########################
############################################################

st.title(f"Parabolic Trajectory Plotter{ch.EMOJI_BEGIN}")

col_1, col_2 = st.columns(2)

# Get the mass
mass = col_1.number_input("Mass (Kg)", min_value=0)

# Get the initial velocity
v_0 = col_1.number_input("Initial Velocity (m/s)", min_value=0)

# Get the angle
theta = col_1.number_input("Launch angle (°)", min_value=0, max_value=180)

########################## CALCULATION ##########################
#################################################################

t_flight = calc_t_flight(v_0, theta) # Flight time
max_range = calc_range(v_0, theta) # Max range
h_max = calc_h_max(v_0, theta) # Max height
t_h_max = calc_t_h_max(v_0, theta) # Time for max height
max_height_x = calc_x_t(t_h_max, v_0, theta) # X position for max height
max_height_y = calc_y_t(t_h_max, v_0, theta) # Y position for max height

########################## METRICS ##########################
#############################################################

col_1, col_2, col_3, col_4 = st.columns(4)

col_2.metric(label='Max range', value=f'{max_range:.3f} m')
col_1.metric(label='Time of flight', value=f'{t_flight:.3f} s')
col_3.metric(label='Max height', value=f'{h_max:.3f} m')
col_4.metric(label='Time to max height', value=f'{t_h_max:.3f} s')

########################## PLOTS ##########################
###########################################################

# Time step interval
interval = 0.001

# Time stamps
time_values = np.arange(0, np.ceil(t_flight), interval)
time_values = list(time_values)
# print(f'time_values: {time_values.shape}')

# Arrays to store x and y positions at each time step
v_x_array = []
v_y_array = []

for i, t in enumerate(time_values):
    v_x = calc_x_t(t, v_0, theta)
    v_y = calc_y_t(t, v_0, theta)

    if v_y < 0:
      # np.delete(time_values, i)
      # time_values.remove(t)
      continue
    
    v_x_array.append(v_x)
    v_y_array.append(v_y)

# print(f'time_values: {time_values.shape}')

# Plot the v_x vs v_y
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(v_x_array, v_y_array, label="Trajectory")
ax.plot(max_height_x, max_height_y, 'ro', label=f'Max Height ({max_height_x:.3f}, {max_height_y:.3f})')

ax.set_title("Projectile Motion with Air Resistance")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# Plot the trajectory using matplotlib
fig, ax = plt.subplots(figsize=(8, 6))
# time_values = list(time_values)
ax.plot(time_values[:len(v_y_array)], v_y_array, label="Trajectory")
ax.plot(max_height_x, max_height_y, 'ro', label=f'Max Height ({max_height_x:.3f}, {max_height_y:.3f})')

ax.set_title("Projectile Motion with Air Resistance")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# Calculate velocities over time
v_x_array_velocity = [v_0 * np.cos(np.radians(theta))] * len(time_values)
v_y_array_velocity = [v_0 * np.sin(np.radians(theta)) - g * t for t in time_values]

# Plot velocity vs time
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(time_values, v_x_array_velocity, label="Horizontal Velocity (v_x)", color='blue')
ax.plot(time_values, v_y_array_velocity, label="Vertical Velocity (v_y)", color='green')
ax.set_title("Velocity vs Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Velocity (m/s)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Vertical acceleration is constant at -g
g_values = [-g] * len(time_values)
horizontal_acceleration = [0] * len(time_values)

# Plot acceleration vs time
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(time_values, g_values, label="Vertical Acceleration", color='red')
ax.plot(time_values, horizontal_acceleration, label="Horizontal Acceleration", color='purple', linestyle='--')
ax.set_title("Acceleration vs Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Acceleration (m/s²)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

########################## CALCULATION DETAILS ##########################
#########################################################################

st.markdown(f'## Calculation Details')
a: int = 10
b: int = 5
st.latex(fr'\frac{a}{b}')
st.write(f'Initial velocity ($v_0$) $= \\frac{a}{b}$')

