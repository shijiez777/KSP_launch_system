import math
import time
import krpc

G = 9.8

def shifted_sigmoid_thrust(velocity):
    return 1 / (1 + math.e **-(velocity - 5))

def minimum_thrust_to_negate_gravity(vessel):
    gravitational_force = vessel.mass * vessel.flight().g_force * G
    equilibrium_thrust = gravitational_force / vessel.available_thrust
    return equilibrium_thrust


conn = krpc.connect(name='Sub-orbital flight')

# launch preparation
vessel = conn.space_center.active_vessel
vessel.control.sas = True
# data stream
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
surface_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
TARGET_ALTITUDE = 100 + altitude()
LANDING_VELOCITY = -3

# lift to height
vessel.control.throttle = 1
vessel.control.activate_next_stage()


# Disable engines when target apoapsis is reached
while apoapsis() < TARGET_ALTITUDE:
    pass
print("Target apoapsis reached")
vessel.control.throttle = 0.0
time.sleep(3)
vessel.control.sas_mode = conn.space_center.SASMode.retrograde

#conn.space_center.SASMode.retrograde
print("pointing to retrograde")
print(vessel.control.sas_mode)

# dumb normalization
# max_vertical = -7
# min_vertical = -6
# velo_range = 1
# while surface_altitude() > 3:
#     # print(surface_altitude())
#     curr_velo = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed
#     # print(curr_velo)
#     if curr_velo < -6.:
#         if curr_velo < max_vertical:
#             max_vertical = curr_velo
#             velo_range = abs(max_vertical - min_vertical)
#         throt = abs(curr_velo - min_vertical)/velo_range
#         vessel.control.throttle = throt
#     # print(throt)


while surface_altitude() > 3:
    # print(surface_altitude())
    curr_velo = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed
    # print(curr_velo)
    if curr_velo < LANDING_VELOCITY:
        throt = shifted_sigmoid_thrust(abs(curr_velo))# abs(curr_velo - min_vertical)/velo_range
        vessel.control.throttle = throt
    # print(throt)




vessel.control.throttle = 0
vessel.control.sas = False
print('Landed!')

