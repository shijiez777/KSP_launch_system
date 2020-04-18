import krpc
connection = krpc.connect()

vessel = connection.space_center.active_vessel
vessel.control.activate_next_stage()
