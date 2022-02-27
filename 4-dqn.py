#!/usr/bin/env python
# coding: utf-8

# In[5]:


import glob
import os
import sys


import carla
import random
import cv2
import skimage.measure as measure

#in synchronous mode, sensor data must be added to a queue
import queue
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
from scipy.spatial import distance

IM_WIDTH = 800
IM_HEIGHT = 800


# In[6]:


actor_list = []


# In[7]:


client = carla.Client('localhost', 2000)
client.set_timeout(5.0)


# In[8]:


#print(client.get_available_maps())


# In[9]:


world = client.load_world("Town01")
settings = world.get_settings()
#settings.fixed_delta_seconds = 0.05 
settings.synchronous_mode = False 
world.apply_settings(settings)


# In[10]:




# In[12]:


blueprint_library = world.get_blueprint_library()
bp = random.choice(blueprint_library.filter('vehicle')) # lets choose a vehicle at random
# lets choose a random spawn point
transform = random.choice(world.get_map().get_spawn_points()) 
#spawn a vehicle
vehicle = world.spawn_actor(bp, transform) 
actor_list.append(vehicle)
vehicle.set_autopilot(True)


# In[16]:





# In[40]:


def process_img(image):
    
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, -1))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey()
    return i3/255.0


# In[41]:


camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_transform = carla.Transform(carla.Location(x=2, z=1))
camera_bp.set_attribute('image_size_x', f'{IM_WIDTH}')
camera_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
camera_bp.set_attribute('fov', '90')
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
image_queue = queue.Queue()
camera.listen(lambda data: process_img(data))
actor_list.append(camera)
import time
time.sleep(10)
camera.listen(lambda data: process_img(data))
time.sleep(2)
# In[ ]:



print('destroying actors')
for actor in actor_list:
    actor.destroy()
    print('done.')



