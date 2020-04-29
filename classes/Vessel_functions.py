# import krpc
import math
from functools import partial

def shifted_sigmoid_thrust(self):
    return 1 / (1 + math.e **-(self.velocity - 5))

def minimum_thrust(self):
    """
    Minimum thrust to maintain position in atmosphere
    """
    # g_force includes all forces including thrust and gravitational force
    # mg = vessel.mass * vessel.flight().g_force * 9.8
    surface_gravity = self.orbit.body.surface_gravity
    mg = self.mass * surface_gravity
    equilibrium_thrust = mg / self.available_thrust_stream()
    return equilibrium_thrust

def available_acceleration(self):
    # thrust(F) - mg = ma
    # return a
    surface_gravity = self.orbit.body.surface_gravity

    mg = self.mass * surface_gravity
    a = (self.available_thrust_stream() - mg)/self.mass
    # print(a)
    return a

def above_deaccelerate_burn_height(self):
    """
    Return if deaccelerate burn altitude reached.
    compare deaccelerate burn distance mean_altitude
    """
    # v - at = 0
    # h = vt - 1/2 * a * t^2
    a = available_acceleration(self)
    vertical_v = abs(self.vertical_velocity())
    t = vertical_v / a
    deacceleration_distance = vertical_v * t - 1/2 * a * t ** 2
    # print(deacceleration_distance + 10)
    # print(self.surface_altitude())
    return self.surface_altitude() > deacceleration_distance + 10

def vessel_add_methods_and_attributes(vessel, conn):
    # data streams
    vessel.apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    vessel.mean_altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    vessel.surface_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
    vessel.vertical_velocity = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), "vertical_speed")        

    # vessel.available_thrust = conn.add_stream(getattr, vessel.available_thrust())
    vessel.available_thrust_stream = conn.add_stream(getattr, vessel, "available_thrust")


# vessel = conn.space_center.active_vessel
# refframe = vessel.orbit.body.reference_frame
# with conn.stream(vessel.position, refframe) as position:
#     while True:
#         print(position())


    vessel.terminal_velocity = conn.add_stream(getattr, vessel.flight(), 'terminal_velocity')
    vessel.reynolds_number = conn.add_stream(getattr, vessel.flight(), 'reynolds_number')


    # distance to hard surface
    vessel.bedrock_altitude = conn.add_stream(getattr, vessel.flight(), 'bedrock_altitude')
    # vessel.elevation = conn.add_stream(getattr, vessel.flight(), 'elevation')


    vessel.drag = conn.add_stream(getattr, vessel.flight(), 'drag')
    vessel.aerodynamic_force = conn.add_stream(getattr, vessel.flight(), 'aerodynamic_force')
    vessel.terminal_velocity = conn.add_stream(getattr, vessel.flight(), 'terminal_velocity')





    # attributes
    vessel.TOUCHDOWN_VELOCITY = 1
    vessel.TOUCHDOWN_HEIGHT = 2
    vessel.DEACCELERATE_SEQ_HEIGHT = 10000

    # methods
    vessel.minimum_thrust = partial(minimum_thrust, vessel)
    vessel.available_acceleration = partial(available_acceleration, vessel)
    vessel.above_deaccelerate_burn_height = partial(above_deaccelerate_burn_height, vessel)