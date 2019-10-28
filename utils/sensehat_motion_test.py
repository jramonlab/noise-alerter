#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##############################################################################################TSimple test for acceleration
##############################################################################################
import time
from sense_hat import SenseHat


##############################################################################################
# SENSE-HAT config

sh = SenseHat()

print("\nMotion Module Started...")

max_x = 0
max_y = 0
max_z = 0

LIMIT = 1.5
shock_counter = 0
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
        shock_counter = shock_counter + 1

    print("x={0}, y={1}, z={2}   MAX...x={3}, y={4}, z={5}...SHOCKS={6} ".format(x, y, z, max_x, max_y, max_z, shock_counter))