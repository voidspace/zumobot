from zumo_2040_robot import robot
import time

def sleep_ms(ms):
    time.sleep(ms / 1000)

def stop():
    motors.set_speeds(0, 0)
    motors.off()
    

rgb_leds = robot.RGBLEDs()
motors = robot.Motors()
buzzer = robot.Buzzer()
display = robot.Display()

MAX = motors.MAX_SPEED
STEP = MAX // 100

left = STEP * 25
right = STEP * 25

display.fill(1)
display.text("Starting", 0, 0, 0)
display.show()

buzzer.play("L16 o4 cfa>cra>c4r4")

motors.set_speeds(left, right)
sleep_ms(1500)
motors.set_speeds(-left, -right)
sleep_ms(1500)
stop()