import machine, network, ntptime, time, esp32
from machine import Pin, Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
from time import sleep

if machine.wake_reason() == 2:
    print("Woke up due to EXT0 wake-up.")
elif machine.wake_reason() == 4:
    print('Woke up due to timer wake-up')
else:
    pass

def connectWifi():
    ssid = ''    #Insert Wifi network name here
    pword = ''    #Insert Wifi network password here
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.scan()
    if not wlan.isconnected():
        wlan.connect(ssid, pword)
        while not wlan.isconnected():
            pass
    print('Connected to', wlan.config('ssid'))
    print('IP Address:', wlan.ifconfig()[0])

rtc = RTC()


def dispDateTime(tim):
    year, month, day, wkday, hour, minute, sec, millisec = rtc.datetime()
    if ((month==3 and (day>12 or day==12 and hour >=6)) or (month>=4 and month<11) or (month==11 and (day<5 or day==5 and hour<6))):
        if hour < 4:
            print('Date: {0:0=2d}'.format(month) + '/{0:0=2d}'.format(day - 1) + '/' + str(year))
            curTime = "Time: {0:0=2d}".format(24-(4-hour))+":{0:0=2d}".format(minute)+":{0:0=2d}".format(sec)+" HRS"
            print(curTime)
        else:
            print('Date: {0:0=2d}'.format(month) + '/{0:0=2d}'.format(day) + '/' + str(year))
            curTime = "Time: {0:0=2d}".format(hour - 4) + ":{0:0=2d}".format(minute) + ":{0:0=2d}".format(sec) + " HRS"
            print(curTime)
    else:
        if hour < 5:
            print('Date: {0:0=2d}'.format(month) + '/{0:0=2d}'.format(day - 1) + '/' + str(year))
            curTime = "Time: {0:0=2d}".format(24-(5-hour))+":{0:0=2d}".format(minute)+":{0:0=2d}".format(sec)+" HRS"
            print(curTime)
        else:
            print('Date: {0:0=2d}'.format(month) + '/{0:0=2d}'.format(day) + '/' + str(year))
            curTime = "Time: {0:0=2d}".format(hour - 5) + ":{0:0=2d}".format(minute) + ":{0:0=2d}".format(sec) + " HRS"
            print(curTime)

tim = Timer(0)
tim.init(mode=Timer.PERIODIC, period=15000, callback=dispDateTime)


neo_board = Pin(0, Pin.OUT)
neo_power = Pin(2, Pin.OUT)
neo_power.value(1)
np = NeoPixel(neo_board, 1)

touch = TouchPad(Pin(14))

def readTouch(touchTim):
    if touch.read() < 630:
        np[0] = (0, 100, 0)
        np.write()
    else:
        np[0] = (0, 0, 0)
        np.write()
        
touchTim = Timer(1)
touchTim.init(mode=Timer.PERIODIC, period=50, callback=readTouch)

def sleepy(red):
    print('I am going to sleep for 1 minute')
    led_board.value(0)
    deepsleep(60000)
    led_board.value(1)
    

    
    
led_board = Pin(13, Pin.OUT)
led_board.value(1)

red = Timer(2)
button = Pin(26, Pin.IN)
esp32.wake_on_ext0(pin=button, level=esp32.WAKEUP_ANY_HIGH)
red.init(mode=Timer.PERIODIC, period=30000, callback=sleepy)

connectWifi()
ntptime.settime()

while True:
    pass
