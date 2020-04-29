import sys
sys.path.append('../classes')

import time
import krpc
from Vessel_functions import vessel_add_methods_and_attributes


if __name__ == "__main__":

    conn = krpc.connect(name='Sub-orbital flight')
    vessel = conn.space_center.active_vessel

    # launch preparation
    vessel_add_methods_and_attributes(vessel, conn)

    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    vessel.auto_pilot.engage()
    vessel.control.throttle = 1
    time.sleep(1)

    # lift off
    print('Launch!')

    print(vessel.terminal_velocity())

    vessel.control.activate_next_stage()

    # Booster
    # fuel_amount = conn.get_call(vessel.resources.amount, 'SolidFuel')
    # expr = conn.krpc.Expression.less_than(
    #     conn.krpc.Expression.call(fuel_amount),
    #     conn.krpc.Expression.constant_float(0.1))
    # event = conn.krpc.add_event(expr)
    # with event.condition:
    #     event.wait()
    # print('Booster separation')
    # vessel.control.activate_next_stage()

    # Apoapsis
    mean_altitude = conn.get_call(getattr, vessel.flight(), 'mean_altitude')
    expr = conn.krpc.Expression.greater_than(
        conn.krpc.Expression.call(mean_altitude),
        conn.krpc.Expression.constant_double(10000))
    event = conn.krpc.add_event(expr)
    with event.condition:
        event.wait()

    # change heading, pitch 60, heading 90(west).
    print('Gravity turn')


    print(vessel.terminal_velocity())


    vessel.auto_pilot.target_pitch_and_heading(60, 90)

    # wait till reaching 100km apoapsis and stop throttle. Jettison the launch stage and turn of autopilot
    apoapsis_altitude = conn.get_call(getattr, vessel.orbit, 'apoapsis_altitude')
    expr = conn.krpc.Expression.greater_than(
        conn.krpc.Expression.call(apoapsis_altitude),
        conn.krpc.Expression.constant_double(100000))
    event = conn.krpc.add_event(expr)
    with event.condition:
        event.wait()

    print('Launch stage separation')

    print(vessel.terminal_velocity())

    vessel.control.throttle = 0
    time.sleep(1)
    vessel.control.activate_next_stage()
    vessel.auto_pilot.disengage()

    # reaching apoapsis
    while vessel.vertical_velocity() > 0:
        pass
    print("apoapsis reached")

    print(vessel.terminal_velocity())


    vessel.control.sas = True
    vessel.control.rcs = True
    time.sleep(0.1)
    vessel.auto_pilot.sas_mode = conn.space_center.SASMode.retrograde

    time.sleep(3)
    print("pointing to retrograde")
    print(vessel.terminal_velocity())


    while vessel.surface_altitude() > vessel.DEACCELERATE_SEQ_HEIGHT:
        pass

    print("Starting deaccelerate burn")
    print(vessel.terminal_velocity())

    ## landing
    while vessel.above_deaccelerate_burn_height():
        pass
    print("Deaccelerate height reached, ", vessel.mean_altitude())
    vessel.control.throttle = 1
    print(vessel.terminal_velocity())

    # while surface_altitude() > 3:
    #     print(surface_altitude())
    #     pass


    while abs(vessel.vertical_velocity()) > 3:
        # print(vessel.vertical_velocity())
        pass

    vessel.control.throttle = 0
    
    vessel.control.sas = False
    print('Landed!')
    print(vessel.terminal_velocity())


    # srf_altitude = conn.get_call(getattr, vessel.flight(), 'surface_altitude')
    # expr = conn.krpc.Expression.less_than(
    #     conn.krpc.Expression.call(srf_altitude),
    #     conn.krpc.Expression.constant_double(1000))
    # event = conn.krpc.add_event(expr)
    # with event.condition:
    #     event.wait()

    # vessel.control.activate_next_stage()

    # while vessel.flight(vessel.orbit.body.reference_frame).vertical_speed < -0.1:
    #     print('Altitude = %.1f meters' % vessel.flight().surface_altitude)
    #     time.sleep(1)
    # print('Landed!')