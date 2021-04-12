from time import sleep
from djitellopy import tello

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

#Basic Movements
drone.takeoff()
drone.send_rc_control(0, 50, 0, 0)
sleep(10)
drone.send_rc_control(0, 0, 0, 30)
sleep(10)
drone.send_rc_control(0, 0, 0, 0)
drone.land()


