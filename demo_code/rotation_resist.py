# This demo shows how the Zumo can use its gyroscope to detect when it is being
# rotated, and use the motors to resist that rotation.
#
# Do not move the robot while it says "Calibrating..." on the screen.
#
# After the calibration is done, press button A to start the motors.
# If you try to turn the Zumo, or put it on a surface that is turning, it will
# drive its motors to counteract the turning.  This demo only uses the Z axis
# of the gyro, so it is possible to pick up the Zumo, rotate it about its X
# and Y axes, and then put it down facing in a new position.
#
# This example is similar to gyro_turn.py.

from zumo_2040_robot import robot
import time

motors = robot.Motors()
button_a = robot.ButtonA()
button_c = robot.ButtonC()
display = robot.Display()
yellow_led = robot.YellowLED()

display.fill(0)
display.text("Starting IMU...", 0, 0, 1)
display.show()
imu = robot.IMU()
imu.reset()
imu.enable_default()

max_speed = 6000
kp = 350
kd = 7

display.fill(0)
display.text("Calibrating...", 0, 0, 1)
display.show()
time.sleep_ms(500)
calibration_start = time.ticks_ms()
stationary_gz = 0.0
reading_count = 0
while time.ticks_diff(time.ticks_ms(), calibration_start) < 1000:
    if imu.gyro.data_ready():
        imu.gyro.read()
        stationary_gz += imu.gyro.last_reading_dps[2]
        reading_count += 1
stationary_gz /= reading_count

drive_motors = False
last_time_gyro_reading = None
turn_rate = 0.0    # degrees per second
robot_angle = 0.0  # degrees

def draw_text():
    display.fill(0)
    if drive_motors:
        display.text("A: Stop motors", 0, 0, 1)
    else:
        display.text("A: Start motors", 0, 0, 1)
    display.text(f"Angle:", 0, 32, 1)

draw_text()

while True:
    # Update the angle and the turn rate.
    if imu.gyro.data_ready():
        imu.gyro.read()
        turn_rate = imu.gyro.last_reading_dps[2] - stationary_gz  # degrees per second
        now = time.ticks_us()
        if last_time_gyro_reading:
            dt = time.ticks_diff(now, last_time_gyro_reading)
            robot_angle += turn_rate * dt / 1000000
        last_time_gyro_reading = now

    # If the user presses button A, toggle whether the motors are on.
    if button_a.check() == True:
        while button_a.check() != False: pass  # wait for release
        drive_motors = not drive_motors
        if drive_motors:
            display.fill(1)
            display.text("Starting", 30, 20, 0)
            display.text("WATCH OUT", 27, 30, 0)
            display.show()
            time.sleep_ms(500)
        draw_text()
        last_time_gyro_reading = time.ticks_us()

    # Show the current angle in degrees.
    display.fill_rect(48, 32, 72, 8, 0)
    display.text(f"{robot_angle:>9.3f}", 48, 32, 1)
    display.show()

    # Drive motors.
    if drive_motors:
        turn_speed = -robot_angle * kp - turn_rate * kd
        if turn_speed > max_speed: turn_speed = max_speed
        if turn_speed < -max_speed: turn_speed = -max_speed
        motors.set_speeds(-turn_speed, turn_speed)
    else:
        motors.off()

    yellow_led.value(drive_motors)
