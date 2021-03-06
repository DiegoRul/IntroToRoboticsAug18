from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
import time
from pymavlink import mavutil
import Tkinter as tk
vehicle = connect("udp:localhost:14551",wait_ready=True)

def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED, 0b0000111111000111, 
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

def arm_and_takeoff(vehicle, TargetAltitude):

    while not vehicle.is_armable:
        print("drone unarmable, waiting...")
        time.sleep(1)

    print("guided mode on...")
    vehicle.mode = VehicleMode("GUIDED")
    print("WARNING, motors arming")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting arming...")
        time.sleep(1)
    print("WARNING: Taking off.")
    vehicle.simple_takeoff(TargetAltitude)

    while True:
        currentaltitude = vehicle.location.global_relative_frame.alt
        print("Altitude: %f"% currentaltitude)

        if currentaltitude >= (TargetAltitude*0.95):
            print("Altitude Reached. Takeoff Finished")
            break
        time.sleep(1)
def key(event):
    if event.char == event.keysym:
        if event.keysym == 'l':
            vehicle.mode = VehicleMode("LAND")
        else:
            if event.keysym == 'w':
                set_velocity_body(vehicle, 10, 0, 0)
                print("vehicle moving foward")
            elif event.keysym == 's':
                set_velocity_body(vehicle, -10, 0, 0)
                print("vehicle moving backwards")
            elif event.keysym == 'a':
                set_velocity_body(vehicle, 0, -10, 0)
                print("vehicle moving leftwards")
            elif event.keysym == 'd':
                set_velocity_body(vehicle, 0, 10, 0)
                print("vehicle moving rightwards")
            


def main():
    
    arm_and_takeoff(vehicle, 10)
    root =tk.Tk()
    print("arrow control, press l to land")
    root.bind_all('<Key>', key)
    root.mainloop()
    

if __name__ == "__main__":
    main()