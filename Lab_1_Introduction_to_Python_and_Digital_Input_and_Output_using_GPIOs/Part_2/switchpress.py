from machine import Pin
from neopixel import NeoPixel
from time import sleep

# Onboard RGB LED is connected to IO_0
# Create output pin on GPIO_0
led_board = Pin(0, Pin.OUT)
led_power = Pin(2, Pin.OUT)
led_power.value(1) #turns on RGB LED
np = NeoPixel(led_board, 1)

push_button = Pin(38, Pin.IN)

numPressed = 0
while numPressed < 5:
    logic_state = push_button()
    if logic_state == False: 
        np[0] = (0, 60, 0)
        np.write()
        numPressed += 1
        sleep(0.3)
    else:           
        np[0] = (60, 0, 0)
        np.write()
        
np[0] = (0, 0, 0)
np.write()
print("You have successfully implemented LAB1!")