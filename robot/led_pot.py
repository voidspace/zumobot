import machine
import utime

LED = machine.PWM(machine.Pin(16))
LED.freq(100)
switch = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
pot = machine.ADC(26)

main_led = machine.Pin(25, machine.Pin.OUT)
#LED = machine.Pin(16, machine.Pin.OUT)


button = False

def switch_irq(pin):
    global button
    button = not button
    
switch.irq(trigger=machine.Pin.IRQ_FALLING, handler=switch_irq)

value = pot.read_u16()
while True:
    last = value
    new  = pot.read_u16()
    value = (last + new) // 2
    print(new, value)
    main_led.value(int(button))
    if button:
        LED.duty_u16(value)
    else:
        LED.duty_u16(0)
    
    utime.sleep_ms(100)
        
        
        


