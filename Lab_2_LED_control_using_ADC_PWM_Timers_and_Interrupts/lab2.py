import machine
from machine import Pin, RTC, Timer, PWM, ADC

year = int(input('Year? '))
month = int(input('Month? '))
day = int(input('Day? '))
weekday = int(input('Weekday? '))
hour = int(input('Hour? '))
minute = int(input('Minute? '))
sec = int(input('Second? '))
microsec = int(input('Microsecond? '))

counter = 0

rtc = machine.RTC()
rtc.init((year, month, day, weekday, hour, minute, sec, microsec))

def dispTime(tim):
    print(rtc.datetime())#curTime)#use rtc.datetime to print time

tim = Timer(0)
tim.init(mode=Timer.PERIODIC, period=30000, callback=dispTime)

def readInput(analogTim):
        global counter
        potVal = adc.read() / 4095
        if counter%2!=0:
            pwm.freq(int((potVal+1) * 15))
        else:
            if counter!=0:  
                pwm.duty_u16(int(potVal*1024))
        return 

pot = Pin(36, Pin.IN)
adc = ADC(pot)
analogTim = Timer(1)
analogTim.init(mode=Timer.PERIODIC, period=100, callback=readInput)

led = Pin(27, Pin.OUT)

def push_update(buttonPress):
    global counter
    counter += 1
    return

pwm = PWM(led, freq=10, duty=512)
buttonPress = Pin(38, Pin.IN, Pin.PULL_UP)
buttonPress.irq(trigger=Pin.IRQ_RISING, handler=push_update)

while True:
    pass
