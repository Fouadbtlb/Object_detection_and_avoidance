import os
from os import listdir
from os.path import isfile, join
paths = {
    'WORKSPACE_PATH': os.path.join('Pytorch', 'workspace'),
    'SCRIPTS_PATH': os.path.join('Pytorch','scripts'),
    'APIMODEL_PATH': os.path.join('Pytorch','models'),
    'ANNOTATION_PATH': os.path.join('Pytorch', 'workspace','annotations'),
    'IMAGE_PATH': os.path.join('Pytorch', 'workspace','images'),
    'MODEL_PATH': os.path.join('Pytorch', 'workspace','models'),
    'PRETRAINED_MODEL_PATH': os.path.join('Pytorch', 'workspace','pre-trained-models'),
    'PROTOC_PATH':os.path.join('Pytorch','protoc')
 }
paths['ANNOTATION_TRAIN_PATH']=os.path.join(paths['ANNOTATION_PATH'],"train")
paths['ANNOTATION_TEST_PATH']=os.path.join(paths['ANNOTATION_PATH'],"test")
paths['ANNOTATION_VAL_PATH']=os.path.join(paths['ANNOTATION_PATH'],"val")
