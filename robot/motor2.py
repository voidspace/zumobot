import machine
import time
import math

main_led = machine.Pin(25, machine.Pin.OUT)
motor_control = machine.PWM(machine.Pin(15))
motor_control.freq(100)
pot = machine.ADC(26)

count = 0
state = True
while True:
    count += 1
    if not count % 100:
        state = not state
        main_led.value(int(state))

    val = pot.read_u16()
    motor_control.duty_u16(val)

    time.sleep_ms(20)
