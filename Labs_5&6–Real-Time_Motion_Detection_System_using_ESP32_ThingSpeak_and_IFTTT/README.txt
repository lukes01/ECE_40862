I connect from the ESP32 to the MPU 6050 via a Stemma QT to Stemm QT connector 
cable. I then utilize the Channel 0 of the connection utilizing pin 20 as the
serial clock and pin 22 as the serial data channel. After attempting to 
connect to the MPU 6050 over I2C, if the inital connection is not successOful 
I retry the connection until it succeeds. Upon successful connection, a 
message saying that the microcontroller is connected to the sensor. I then 
set up the sensor by writing to the power, sample rate, configuration, and 
accelerometer configuration registers. I then connect to my Wifi network, and
 if the device does not originally connect, the device continuously tries to 
connect. Upon successful connection, the device reads the acceleration in 
the X, Y, Z direction and calibrates the data. I then print that the device
 is calibrated and intialize a timer that reads a thingspeak channel every 30
 seconds. A '1' or '0' is sent via activation from Google Assistant. When the
 device reads a '1' from the thingspeak channel, the device
 is now activated and reads the acceleration every second using a hardware 
timer. Upon motion, the onboard red LED turns on and the ESP32 sends a 
notification with the difference in acceleration to my phone. Upon reading 
'0', the onboard red LED turns off and the device stops reading the 
acceleration values.


Youtube link: https://youtu.be/n_DaXjnB_jk