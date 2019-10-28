#!/usr/bin/env python
# coding: utf-8

# # GPIO TEST
# 
# LED on pin 16 is blinking
# LED on pin 16 is ON as long as the signal on Pin 13 is on
# 
# 
# 

# In[12]:


# gpio_blink.py
# 

import RPi.GPIO as GPIO # requires install on env-> pip install RPi.GPIO
import time
from sense_hat import SenseHat

# sense hat setup
sh = SenseHat()
sh.clear()
sh.show_message(ini_msg,scroll_speed=0.1, text_colour = [100, 100, 100], back_colour = [0, 0, 0])

ALARM_LED_X = 1
ALARM_LED_Y = 1
ALARM_LED_COLOUR =  [255, 0, 0] # RED

# RPI GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(13, GPIO.IN)

state = True

# endless loop, on/off for  500 ms
while True:
	
	sh.set_pixel(ALARM_LED_X, ALARM_LED_Y, ALARM_LED_COLOUR)
	
	GPIO.output(16, True)
	GPIO.output(20, GPIO.input(13))

	time.sleep(0.5)

	GPIO.output(16, False)
	GPIO.output(20, GPIO.input(13))

	sh.clear()
	
	time.sleep(0.5)

	print(GPIO.input(13))


# In[41]:


# Set Leds Off
GPIO.output(16, False)
GPIO.output(20, False)


# In[40]:


# Set Leds On
GPIO.output(16, True)
GPIO.output(20, True)


# In[39]:


# Get signal value
print(GPIO.input(13))

