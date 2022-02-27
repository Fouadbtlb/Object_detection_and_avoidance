


import glob
import os
import sys
import random
import time
import numpy as np
import cv2
import math
from collections import deque
import timm


from keras.applications.xception import Xception
from keras.layers import Dense, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.models import Model


import torch
from  torchvision import models
from paths import *
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import cv2
import carla

CLASSES=["Dog","Motorcycle", "Van", "Bus", "Bicycle", "Car","Person","Man", "Truck"]
SHOW_PREVIEW = False
IM_WIDTH = 640
IM_HEIGHT = 480
SECONDS_PER_EPISODE = 10
REPLAY_MEMORY_SIZE = 5_000
MIN_REPLAY_MEMORY_SIZE = 1_000
MINIBATCH_SIZE = 16
PREDICTION_BATCH_SIZE = 1
TRAINING_BATCH_SIZE = MINIBATCH_SIZE // 4
UPDATE_TARGET_EVERY = 5
MODEL_NAME = "Xception"

MEMORY_FRACTION = 0.8
MIN_REWARD = -200

EPISODES = 100

DISCOUNT = 0.99
epsilon = 1
EPSILON_DECAY = 0.95 
MIN_EPSILON = 0.001

AGGREGATE_STATS_EVERY = 10
class DQNAgent:
    def __init__(self):
        self.model = self.create_model()
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

       
        self.target_update_counter = 0


        self.terminate = False
        self.last_logged_episode = 0
        self.training_initialized = False

    def create_model(self):
        #read the model
        my_faster_rcnn = models.detection.fasterrcnn_mobilenet_v3_large_fpn()
        num_classes = len(CLASSES)
        in_features = my_faster_rcnn.roi_heads.box_predictor.cls_score.in_features
        my_faster_rcnn.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        my_faster_rcnn.load_state_dict(torch.load(join(paths["MODEL_PATH"],"dict_pretrained_faster_rcnn.h"),map_location='cpu'))

        #adapt it
        my_faster_rcnn.roi_heads.box_predictor =nn.Linear(in_features, 3)
        return my_faster_rcnn

    def update_replay_memory(self, transition):
        # transition = (current_state, action, reward, new_state, done)
        self.replay_memory.append(transition)

    def train(self):
        #TO DO

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]

    def train_in_loop(self):
        #to do