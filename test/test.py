import sys
sys.path.append('../classes')

import krpc
import time
from Vessel_functions import vessel_add_methods_and_attributes


conn = krpc.connect(name='Sub-orbital flight')
vessel = conn.space_center.active_vessel
vessel_add_methods_and_attributes(vessel, conn)



while 1:
    # print("mean alt: ", round(vessel.mean_altitude()), ", Surf_alt: ", round(vessel.surface_altitude()), ", bedrock_alt: ", round(vessel.bedrock_altitude()), ", elevation: ", round(vessel.elevation()), end = '\r')
    # print("Drag: ", list(map(round, vessel.drag())), ", aerodynamic force: ", list(map(round, vessel.aerodynamic_force())))
    print("vert Drag: ", list(map(round, vessel.drag()))[0], ", vert velo: ", round(vessel.vertical_velocity()), ", K: ", list(map(round, vessel.drag()))[0]/ (round(vessel.vertical_velocity())**2))

    
    # print(vessel.terminal_velocity())
    time.sleep(1)