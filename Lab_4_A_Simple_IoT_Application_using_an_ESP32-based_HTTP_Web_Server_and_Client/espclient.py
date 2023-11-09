import machine, network, socket, esp32, socket
from machine import Timer
from esp32 import raw_temperature

numRan = 0

def print_Hall_Temp(tim):
    global numRan
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    print('Temperature:' + str(temp))
    print('Hall Sensor:' + str(hall) + '\n')
    sock = socket.socket()
    addr = socket.getaddrinfo("api.thingspeak.com",80)[0][-1]
    sock.connect(addr)
    host = "api.thingspeak.com"
    path = "api_key='''INSERT API KEY HERE'''&field1="+str(temp)+"&field2="+str(hall)
    sock.send(bytes("GET /update?%s HTTP/1.0\r\nHost: %s\r\n\r\n" %(path,host),"utf8"))
    numRan += 1
    sock.close()
    
    
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


connectWifi()

tim = Timer(0)
tim.init(mode=Timer.PERIODIC, period=30000, callback=print_Hall_Temp)

while numRan < 10:
    pass

tim.deinit()
