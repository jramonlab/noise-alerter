#!/usr/bin/env python
# coding: utf-8

# # Creating a Client Instance

# In[ ]:


import paho.mqtt.client as mqtt
import time


# Creating a Client Instance
# The client constructor takes 4 optional parameters, as shown below .but only the client_id is necessary, and should be unique.

# In[ ]:


#Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)

client_name = "client_X1"
client = mqtt.Client(client_name)


# # on_message CALLBACK

# In[3]:


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("\n")


# In[4]:


# Now we need to attach our callback function to our client object as follows:
client.on_message = on_message        #attach function to callback


# # Connecting To a Broker or Server

# Connecting To a Broker or Server
# The method can be called with 4 parameters. The connect method declaration is shown below with the default parameters.
# 
# connect(host, port=1883, keepalive=60, bind_address="")

# In[5]:


#host_name = "test.mosquitto.org"
#host_name = "broker.hivemq.com"
#host_name = "iot.eclipse.org"
#host_name = "192.168.1.138"
host_name = "localhost"

client.connect(host_name)


# # Loop Start

# In[6]:


# and finally we need to run a loop otherwise we won’t see the callbacks. 
# The simplest method is to use loop_start() as follows.
client.loop_start()    #start the loop


# # Subscribing To Topics

# The subscribe method accepts 2 parameters – A topic or topics and a QOS (quality of Service) as shown below with their default values.
# 
# subscribe(topic, qos=0)

# In[7]:


topic = "alerter/sensor-T1"
client.subscribe(topic, qos=0)


# # Publishing Messages

# The publish method accepts 4 parameters. The parameters are shown below with their default values.
# 
# publish(topic, payload=None, qos=0, retain=False)

# In[8]:


client.publish("alerter/sensor-T1","ON")


# In[9]:


# STOP LOOP

time.sleep(25) # wait
client.loop_stop() #stop the loop
print("Loop stopped !")


# In[ ]:





# In[ ]:




