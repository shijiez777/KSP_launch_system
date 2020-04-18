import math
import time
import krpc

TURN_START_ALTITUDE = 250
TURN_END_ALTITUDE = 45000
TARGET_ALTITUDE = 100000
CIRCULARIZATION_BURN_ALTITUDE = 70500

conn = krpc.connect(name = "Launch into orbit")
vessel = conn.space_center.active_vessel

# set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
# stage_4_resources = vessel.resources_in_decouple_stage(stage=4, cumulative=False)
# srb_fuel = conn.add_stream(stage_4_resources.amount, 'SolidFuel')

# pre_launch setup
vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 1.0

for i in range(3, 0, -1):
    print(i, end = '\r')
    time.sleep(1)
print("Launch!")

# launching and pitching

# activate first stage
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)

# Main ascend loop
# srbs_separated = False
turn_angle = 0

while True:
    
    # Gravity turn
    if altitude() > TURN_START_ALTITUDE and altitude() < TURN_END_ALTITUDE:
        frac = ((altitude() - TURN_START_ALTITUDE) / (TURN_END_ALTITUDE - TURN_START_ALTITUDE))
        new_turn_angle = frac * 90
        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)
    
    # separate SRBs when fuel depleted
#     if not srbs_separated:
#         if srb_fuel() < 0.1:
#             vessel.control.activate_next_stage()
#             srbs_separated = True
#             print("SRBs separated")
    
    # Decrease throttle when approaching target apoapsis
    if apoapsis() > TARGET_ALTITUDE * 0.9:
        print("Approaching target apoapsis")
        vessel.control.throttle = 0.25
        break


# Fine tunes apoapsis, using 10% thrust, then waits until the rocket has left Kerbin atmosphere.

# Disable engines when target apoapsis is reached
while apoapsis() < TARGET_ALTITUDE:
    pass
print("Target apoapsis reached")
vessel.control.throttle = 0.0
time.sleep(5)
vessel.control.activate_next_stage()

# wait until out of atmosphere
print("Coasting out of atmosphere")
while altitude() < CIRCULARIZATION_BURN_ALTITUDE:
    pass

# Circularization burn
# plan circularization burn(using vis-viva equation)
print("Planning circularization burn")
# Delta-v calculation
mu = vessel.orbit.body.gravitational_parameter
r = vessel.orbit.apoapsis
a1 = vessel.orbit.semi_major_axis
a2 = r
v1 = math.sqrt(mu *((2./r) - (1./a1)))
v2 = math.sqrt(mu *((2./r) - (1./a2)))
delta_v = v2 - v1

# add maneuver node
node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde = delta_v)

# Burn time calculation(using rocket equation)
F = vessel.available_thrust
Isp = vessel.specific_impulse * 9.82
m0 = vessel.mass
m1 = m0 / math.exp(delta_v/Isp)
flow_rate = F / Isp
burn_time = (m0 - m1) / flow_rate

# Rotate craft and wait till the circularization burn.
# orientate ship
print("orientating ship for circularization burn")
vessel.auto_pilot.reference_frame = node.reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)
vessel.auto_pilot.wait()

# wait till burn, wrap till burn
print("Waiting for the circularization burn")
burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
lead_time = 10
conn.space_center.warp_to(burn_ut - lead_time)

# Circularization burn
# Execute burn
print("Ready to execute burn")
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, "time_to_apoapsis")
while time_to_apoapsis() - (burn_time/2.) > 0:
    pass

print("Executing burn")
vessel.control.throttle = 1.0

time.sleep(burn_time - 0.1)
print("Adjusting burn")
vessel.control.throttle = 0.02
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

while remaining_burn()[1] > 0.01:
    pass
vessel.control.throttle = 0.0
node.remove()

vessel.auto_pilot.disengage()
time.sleep(2)
vessel.control.sas = True
time.sleep(2)
vessel.control.sas_mode = conn.space_center.SASMode.prograde

print("Launch complete")