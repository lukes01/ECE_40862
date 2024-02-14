from machine import Pin, I2C, Timer
import utime, network, socket, json, math, urequests
from neopixel import NeoPixel

#CONSTANTS
PWR_MGMT = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
ACCEL_CONFIG = 0x1C
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
ACCEL_CALIB = 16384
X_CALIB = 0.06
Y_CALIB = 0.015
Z_CALIB = 1
base_x_accel = 0
base_y_accel = 0
base_z_accel = 1

thingSpeak_URL = 'https://api.thingspeak.com/channels/2364710/fields/1.json?api_key=PF6BKZLV1OF3IK1E&results=2'	#thingspeak URL
server = 'http://maker.ifttt.com/trigger/Device_Moved/json/with/key/lUmMiXA5fcADVyYGeHJVBLr_69E5l_EuLkqZ4Ftm5QZ'	#IFTTT url

# Onboard RGB LED is connected to IO_0
# Create output pin on GPIO_0
led_board = Pin(0, Pin.OUT)
led_power = Pin(2, Pin.OUT)
led_power.value(1) #turns on RGB LED
np = NeoPixel(led_board, 1)
red_led = Pin(13, Pin.OUT)	#set up red LED

isOn = '0'

def sendData(runTimer):
    global server 
    accel_x, accel_y, accel_z = get_mpu6050_data(i2c)    
    if abs(accel_x) > base_x_accel or abs(accel_y) > base_y_accel or abs(accel_z) > base_z_accel:
        red_led.value(1)
        accel_data = {"X" : accel_x, "Y": accel_y, "Z" : (accel_z - 1)}
        json_data = json.dumps(accel_data)
        itWorks = urequests.post(server, data=json_data, headers = {'Content-type': 'application/json'})
    else:
        red_led.value(0)
        
def init_mpu6050(i2c, address=0x68):	#Writes to all registers to turn them on
    i2c.writeto_mem(address, PWR_MGMT, b'\x00')	#Writes to power register
    utime.sleep_ms(100)
    i2c.writeto_mem(address, SMPLRT_DIV, b'\x07')	#Writes to sample rate register
    i2c.writeto_mem(address, CONFIG, b'\x00')	#Writes to congifuration register
    i2c.writeto_mem(address, ACCEL_CONFIG, b'\x00')	#Writes to acceleration configuration register
    
def read_raw_data(i2c, addr, address=0x68):		#Reads data from both byte addresses of data
    value = i2c.readfrom_mem(address, addr, 2)[0]
    return value
 
def get_mpu6050_data(i2c):
    accel_x = round((read_raw_data(i2c, ACCEL_XOUT) / ACCEL_CALIB), 2)	#Calibrate to as close to 0 as possible while still
    accel_y = round(read_raw_data(i2c, ACCEL_YOUT) / ACCEL_CALIB - Y_CALIB, 2)	#Calibrate to as close to 0 as possible while still
    accel_z = round((read_raw_data(i2c, ACCEL_ZOUT) / ACCEL_CALIB + Z_CALIB), 2)	#Calibrate to as close to 1 g as possible while still
    
    return accel_x, accel_y, accel_z
    
def isActive(readChannel):
    message = urequests.get(thingSpeak_URL)	#Read from channel
    global isOn
    isOn = message.json()['feeds'][-1]['field1']
    if isOn == '1':
        led_power.value(1) #turns on RGB LED
        np[0] = (0, 60, 0)
        np.write()		#makes RGB LED green
        runTimer = Timer(1)
        runTimer.init(mode=Timer.PERIODIC, period=1000, callback=sendData)
    else:
        np[0] = (0, 0, 0)
        np.write()
        led_power.value(0) #turns off RGB LED
    return 0

i2c = I2C(0, scl=Pin(20), sda=Pin(22), freq=400000, timeout=500000)	#Sets up I2C on ESP32 at pins 20 for the clock and 22 for the data

sensorAddr = i2c.scan()	#Attempts to connect to MPU6050
while not sensorAddr:	#If doesn't immediately connect, retries until it does
    sensorAddr = i2c.scan()
address = sensorAddr[0]
print('Connected to MPU6050')	#Upon successful connection, prints that it is connected

init_mpu6050(i2c)

def connectWifi():
    ssid = 'Rise Resident'
    pword = 'Boilermakers*100'
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
x, y, z = get_mpu6050_data(i2c)
print('Calibrated MPU6050')


readChannel = Timer(0)	#Creates a time
readChannel.init(mode=Timer.PERIODIC, period=30000, callback=isActive)	#Initializes a timer to read ThingSpeak Channel
