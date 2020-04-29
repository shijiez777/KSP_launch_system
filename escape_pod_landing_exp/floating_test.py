import sys
sys.path.append('../classes')

import math
import time
import krpc
from Vessel_functions import vessel_add_methods_and_attributes

if __name__ == "__main__":
    conn = krpc.connect(name='Sub-orbital flight')

    # launch preparation
    vessel = conn.space_center.active_vessel
    vessel_add_methods_and_attributes(vessel, conn)
    

    vessel.control.sas = True
    vessel.TARGET_ALTITUDE = 100 + vessel.mean_altitude()

    print("alt: ", vessel.mean_altitude())

    # lift to height
    vessel.control.throttle = 1
    vessel.control.activate_next_stage()

    # Disable engines when target apoapsis is reached
    while vessel.apoapsis() < vessel.TARGET_ALTITUDE:
        pass
    print("Target apoapsis reached")

    print(vessel.orbit.body.surface_gravity)


    vessel.control.throttle = 0.0
    time.sleep(0.1)
    vessel.control.sas_mode = conn.space_center.SASMode.stability_assist
    time.sleep(0.1)
    print("SAS stability aid engaged")

    print(vessel.orbit.body.surface_gravity)


    while vessel.vertical_velocity() > 0:
        pass
    print("apoapsis reached")

    print(vessel.orbit.body.surface_gravity)

    """
    TODO:
    1. Fine tune thrust, so that when apoapsis reached, gradually add thrust to achieve velocity 0.
    2. maintain altitude by constantly updating thrust to mitigate the fact that the vessel is getting lighter and require less thrust.
    """


    vessel.control.throttle = vessel.minimum_thrust()
    print("Maintaining altitude")

    print(vessel.orbit.body.surface_gravity)


