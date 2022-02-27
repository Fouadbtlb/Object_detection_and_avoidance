import collections
import os
import numpy as np
from tqdm import tqdm
from torchvision import transforms
import sys
import time
from  PIL import Image
import torch.nn as nn
import cv2
import torch
import pandas as pd


def classes_to_int(liste,dic):
    return [*map(dic.get, liste)]

def get_data(input_path):
    found_bg = False
    all_imgs = {}
    classes_count = {}
    class_mapping = {}
    visualise = True
    i = 1
    with open(input_path,'r') as f:
        print('Parsing annotation files')
        for line in f:
            sys.stdout.write('\r'+'idx=' + str(i))
            i += 1

            line_split = line.strip().split(',')
            (filename,x1,y1,x2,y2,class_name) = line_split

            if class_name not in classes_count:
                     classes_count[class_name] = 1
            else:
                    classes_count[class_name] += 1
            if class_name not in class_mapping:
                    class_mapping[class_name] = len(class_mapping)
            if filename not in all_imgs:
                all_imgs[filename] = {}
                img = cv2.imread(filename)
                (rows,cols) = img.shape[:2]
                all_imgs[filename]['filepath'] = filename
                all_imgs[filename]['width'] = cols
                all_imgs[filename]['height'] = rows
                all_imgs[filename]['boxes'] = []
                all_imgs[filename]['labels'] = []
                all_imgs[filename]['image_id'] = []

            all_imgs[filename]['boxes'].append([int(x1), int(y1), int(x2), int(y2)])
            all_imgs[filename]['labels'].append(class_name)
                

        all_data = []
        for key in all_imgs:
            all_data.append(all_imgs[key])
        # make sure the bg class is last in the list
        if found_bg:
            if class_mapping['bg'] != len(sclass_mapping) - 1:
                key_to_switch = [key for key in class_mapping.keys() if class_mapping[key] == len(class_mapping)-1][0]
                val_to_switch = class_mapping['bg']
                class_mapping['bg'] = len(class_mapping) - 1
                class_mapping[key_to_switch] = val_to_switch

        return all_data, classes_count, class_mapping

class Mydataset(torch.utils.data.Dataset):
    def __init__(self, df_path, height=700, width=700, transforms=None):
        self.transforms = transforms
        self.all_data, _, self.class_mapping=get_data(df_path)
        self.df = pd.DataFrame.from_dict(self.all_data)
        self.height = height
        self.width = width
        self.image_info = collections.defaultdict(dict)
        
        counter=0
        for index, row in tqdm(self.df.iterrows(), total=len(self.df)):
            image_id = str.split(os.path.basename(row['filepath']),".")[0]
            image_path = row['filepath']
            if os.path.exists(image_path):
                self.image_info[counter]["image_id"] = image_id
                self.image_info[counter]["image_path"] = image_path
                self.image_info[counter]["boxes"]=row["boxes"]
                self.image_info[counter]["labels"]=classes_to_int(row["labels"],self.class_mapping)
                counter+=1
        classes_to_int(row["labels"],self.class_mapping)
    def get_class_map(self):
        return self.class_mapping


    def __getitem__(self, idx):
        # load images ad masks
        img_path = self.image_info[idx]["image_path"]
        img = Image.open(img_path).convert("RGB")
        #img = img.resize((self.width, self.height), resample=Image.BILINEAR)
        # processing part and extraction of boxes is left as an exercise to the reader
        
        target = {}
        target["boxes"] = torch.as_tensor(self.image_info[idx]["boxes"], dtype=torch.float32)
        

        target["labels"] =torch.as_tensor(self.image_info[idx]["labels"], dtype=torch.int64)
        target["image_id"]= torch.tensor([idx])
            
        if self.transforms is not None:
            img= self.transforms(img)
            img = torch.unsqueeze(img, 0)
        return transforms.ToTensor()(img),target
    def __len__(self):
        return len(self.image_info)
