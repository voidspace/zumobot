import machine
import time
import math

main_led = machine.Pin(25, machine.Pin.OUT)
motor_control = machine.PWM(machine.Pin(15))
motor_control.freq(100)

while True:
    main_led.value(1)
    for val in range(0, 2 ** 16, 1000):
        motor_control.duty_u16(val)
        time.sleep_ms(50)

    time.sleep(1)

    main_led.value(0)
    for val in range(2 ** 16, 0, -1000):
        motor_control.duty_u16(val)
        time.sleep_ms(50)

    time.sleep(1)
