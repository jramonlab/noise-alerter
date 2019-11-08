#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##############################################################################################
# -Name: gpio_event_collector.py
# -Description: Collects GPIO signal levels and reports to an existing MQTT broker. The
# signal comes from a soun level meter which raise the signal during 12 sec. while the 
# threshold is trespassed. The high oulse is filterd so an only HIGH value is reported
# -Developer: RHZ
# -Date: 28/9/2019
# -Version: 1.0.1
# -Notes:
#         - It needs exception handling when MQTT broker does not connect
##############################################################################################

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from sense_hat import SenseHat
import time

##############################################################################################
#
# MQTT client definition
client_name = "client_X1_nAlerter"
broker_name = "localhost"
broker_port = 1883									# 1883 as default
topic = "site1/area1/device1/sensor1/gpio-alarm"
qos = 0
retain = False
payload = ("LOW", "HIGH")
##############################################################################################
#
# GPIO DEFINITION
# inputs
GPIO_ALARM = 13
# outputs:
GPIO_LED_1 = 16 # GPIO STATE
GPIO_LED_2 = 20 # MQTT CONNECTION OK (ON)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_LED_1, GPIO.OUT)
GPIO.setup(GPIO_LED_2, GPIO.OUT)
GPIO.setup(GPIO_ALARM, GPIO.IN)
##############################################################################################
##############################################################################################
#
# SENSE-HAT config
# Set LED orientation according to the real orientation
try:
	sh = SenseHat()

	# Set current orientation
	sh = SenseHat()
	acceleration = sh.get_accelerometer_raw()
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['z']

	x=round(x, 0)
	y=round(y, 0)
	z=round(z, 0)

	print("x={0}, y={1}, z={2}".format(x, y, z))

	# Update the rotation of the display depending on which way up the Sense HAT is

	if x  == -1:
	  sh.set_rotation(90)
	elif y == 1:
	  sh.set_rotation(0)
	elif y == -1:
	  sh.set_rotation(180)
	else:
	  sh.set_rotation(270)
except:
	sh = SenseHat()
	sh.set_rotation(180)
################################################################################
#
# Initiate values and LED matrix
#
ini_msg = "Starting..."
sh.clear()
sh.show_message(ini_msg,scroll_speed=0.1, text_colour = [200, 200, 200], back_colour = [0, 0, 0])

ALARM_LED_X = 0
ALARM_LED_Y = 0
ALARM_LED_COLOUR =  [200, 0, 0] 	# RED

MSG_LED_X = 1
MSG_LED_Y = 1
MSG_LED_COLOUR =  [0, 0, 200] 		# BLUE	 (broker up)
MSG_DOWN_LED_COLOUR = [255,100 , 0] 	# YELLOW (broker down)

CLEAR_COLOUR = [0,0,0]
down_counter = 55						# counter for showing connection loss on permanent LED
##############################################################################################

ALARM_PULSE_TIME = 12
delay = 3 # loop latency 

client = mqtt.Client(client_name)

# Set Leds Off
GPIO.output(16, False)
GPIO.output(20, False)

last_gpio_value = GPIO.input(GPIO_ALARM)
first_high_time = 0

################################################################################
# Filter gpio high levels
def filter(current_val, last_val, edge_time):
    state = 0
    if (gpio_val == 1 and last_gpio_value == 1):
        now = time.perf_counter()
        time_since_high_edge = now - edge_time
        if (time_since_high_edge > ALARM_PULSE_TIME):
            state = 1    

    return state
################################################################################


################################################################################


print("\nStarted...")

while(True):

    # Check GPIO
    gpio_val = GPIO.input(GPIO_ALARM)

    # Set LED
    if(gpio_val == 1):
        GPIO.output(GPIO_LED_1, True)
        for i in range(8):  sh.set_pixel(ALARM_LED_X, 7-i, ALARM_LED_COLOUR)
    else:
        GPIO.output(GPIO_LED_1, False)
        for i in range(8): sh.set_pixel(ALARM_LED_X, 7-i, CLEAR_COLOUR)
    
    #
    # HIGH EDGE
    if (gpio_val == 1 and last_gpio_value == 0):
        gpio_state = 1    
        first_high_time = time.perf_counter()
        print("\nALARM ON! at ", time.asctime(time.localtime(time.time())))
    else:
        gpio_state = 0
        #
        # Filter unneeded high values
        gpio_state = filter(gpio_val, last_gpio_value, first_high_time)
    
    last_gpio_value = gpio_val
    
    # Connect
    try:
    	res = client.connect(broker_name, broker_port)
    except:
        print("\nCannot connect with MQTT Broker !")
        sh.set_pixel(MSG_LED_X, MSG_LED_Y, MSG_DOWN_LED_COLOUR)
        if (down_counter < 256) : 
            down_counter = down_counter + 1
        sh.set_pixel(MSG_LED_X + 1, MSG_LED_Y + 1, [down_counter, down_counter, 0])
    else:
        if (res == 0 or res == null):
            GPIO.output(GPIO_LED_2, True)
            sh.set_pixel(MSG_LED_X, MSG_LED_Y, MSG_LED_COLOUR)
	    
	    # Publish
            client.publish(topic, payload[gpio_state], qos, retain)
	    
	    # Disconnect
            client.disconnect()
		
    time.sleep(0.025)
    # Clear Leds
    GPIO.output(GPIO_LED_2, False)
    sh.set_pixel(MSG_LED_X, MSG_LED_Y, CLEAR_COLOUR)

    time.sleep(delay)

print("\n...Stopped")



