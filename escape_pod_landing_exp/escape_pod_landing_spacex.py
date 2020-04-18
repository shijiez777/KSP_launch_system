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
    vessel.TARGET_ALTITUDE = 100 + vessel.altitude()

    # lift to height
    vessel.control.throttle = 1
    vessel.control.activate_next_stage()

    # Disable engines when target apoapsis is reached
    while vessel.apoapsis() < vessel.TARGET_ALTITUDE:
        pass
    print("Target apoapsis reached")
    vessel.control.throttle = 0.0
    time.sleep(3)

    while vessel.vertical_velocity() > 0:
        pass
    print("apoapsis reached")

    time.sleep(0.1)
    vessel.control.sas_mode = conn.space_center.SASMode.retrograde
    time.sleep(3)
    print("pointing to retrograde")


    while vessel.above_deaccelerate_burn_height():
        pass

    vessel.control.throttle = 1

    # shut down throttle by altitude
    while vessel.surface_altitude() > vessel.TOUCHDOWN_HEIGHT:
        print(vessel.surface_altitude())
        pass

    # Shut down throttle by velocity
    # while abs(vessel.vertical_velocity()) > vessel.TOUCHDOWN_VELOCITY:
    #     print(vessel.vertical_velocity())
    #     pass

    vessel.control.throttle = 0
    vessel.control.sas = False
    print('Landed!')





    # dumb normalization
    # max_vertical = -7
    # min_vertical = -6
    # velo_range = 1
    # while surface_altitude() > 3:
    #     # print(surface_altitude())
    #     # print(curr_velo)
    #     if curr_velo < -6.:
    #         if curr_velo < max_vertical:
    #             max_vertical = curr_velo
    #             velo_range = abs(max_vertical - min_vertical)
    #         throt = abs(curr_velo - min_vertical)/velo_range
    #         vessel.control.throttle = throt
    #     # print(throt)

    # while surface_altitude() > 3:
    #     # print(surface_altitude())
    #     curr_velo = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed
    #     # print(curr_velo)
    #     if curr_velo < vessel.TOUCHDOWN_VELOCITY:
    #         throt = shifted_sigmoid_thrust(abs(curr_velo))# abs(curr_velo - min_vertical)/velo_range
    #         vessel.control.throttle = throt
    #     # print(throt)




    # vessel.control.throttle = 0
    # vessel.control.sas = False
    # print('Landed!')
