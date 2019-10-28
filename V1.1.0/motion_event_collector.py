#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##############################################################################################
# -Name: motion_event_collector.py
# -Description: Collects motion events from internal sensors and reports to an existing 
#                  MQTT broker.
# -Developer: RHZ
# -Date: 28/9/2019
# -Version: 1.0.0
# -Notes:
#                 - It needs to add some fltering in order to avoid repetitive alasrm 
#                 notifications
##############################################################################################

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from sense_hat import SenseHat
import json


##############################################################################################
#
# MQTT client definition
client_name = "client_X1_nAlerter"
broker_name = "localhost"
broker_port = 1883                                    # 1883 as default
topic = "site1/area1/device1/alarm-vibration/params"
qos = 1
retain = False
payload = ("FALSE", "TRUE")

payload = {"acc_x": "-", "acc_y": "-", "acc_x": "-", "threshold" : "-", "ALARM" : "-"}

#############################################################################################
##############################################################################################
# SENSE-HAT config

sh = SenseHat()

# Ini

##############################################################################################

delay = 0.010 # loop latency 

client = mqtt.Client(client_name)

################################################################################

print("\nMotion Module Started...")

max_x = 0
max_y = 0
max_z = 0

LIMIT = 1.5                # Acceleration LImit to trigger the alarm
shock_counter = 0
alarm_flag = "FALSE"

while True:
    acceleration = sh.get_accelerometer_raw()
    
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x, 1)
    y=round(y, 1)
    z=round(z, 1)
    
    if (max_x < x ): max_x = x
    if (max_y < y ): max_y = y
    if (max_z < z ): max_z = z
    
    if ( abs(x) > LIMIT or abs(y) > LIMIT or abs(z) > LIMIT):
        alarm_flag = "TRUE"
        shock_counter = shock_counter + 1
        print("x={0}, y={1}, z={2}   MAX...x={3}, y={4}, z={5}...SHOCKS={6} ".format(x, y, z, max_x, max_y, max_z, shock_counter))
    else:
        alarm_flag = "FALSE"

    if (alarm_flag == "TRUE"):
        # REPORT ALARM
        # Connect
        try:
            res = client.connect(broker_name, broker_port)
        except:
            print("\nCannot connect with MQTT Broker !")
        else:
            if (res == 0 or res == null):
                
                # Compose payload
                payload["acc_x"] = x
                payload["acc_y"] = y
                payload["acc_z"] = z
                payload["threshold"] = LIMIT
                payload["ALARM"] = alarm_flag
                payload_out = json.dumps(payload)
                
                # Publish
                client.publish(topic, payload_out, qos, retain)
                # Disconnect
                client.disconnect()
                
                time.sleep(2) # temporary delay for avoiding repetitive alarms
                
    time.sleep(delay)


print("\n...Stopped")



