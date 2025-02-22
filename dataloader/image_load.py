import os
from glob import glob
import natsort
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from PIL import Image
import re
import json

from dataloader.utils import *
from lib.utils import *

def get_image_names(mode='train'):

    with open(PATH_PARAMETERS) as f:
        params = json.load(f)
    params = params['models_settings']

    if mode=='train':
        data_dir = params['train_dir']
    if mode=='val':
        data_dir = params['test_dir']

    file_names = []
    temp_dir = os.path.join(data_dir, mode + params['image_folder'], '*')
    print(temp_dir)
    for filename in natsort.natsorted(glob(temp_dir)): 
            file_names.append(os.path.basename(filename))
            
    return file_names

def list_labels(file_names, mode='train'):

    with open(PATH_PARAMETERS) as f:
        params = json.load(f)
    params = params['models_settings']

    # masks = load_masks(file_names,mode=mode)
    shape_to_label = params['label_to_value']
    # print(shape_to_label)
    # label_to_shape = {v:k for k,v in shape_to_label.items()}
    # print(label_to_shape)
    
    # labels = set()
    # for mask in masks:  
    #     labels = labels.union(set([label_to_shape[label] for label in np.unique(mask)]))

    labels = set(shape_to_label.keys())
    return labels

def get_sizes(image_names, mode='train'):

    with open(PATH_PARAMETERS) as f:
        params = json.load(f)
    params = params['models_settings']

    if mode=='train':
        data_dir = params['train_dir']
    if mode=='val':
        data_dir = params['test_dir']

    h = []
    w = []
    
    for image_name in image_names:

        file_name = os.path.join(data_dir, mode+params['image_folder'],  image_name)
        image = np.array(Image.open(file_name))
        
        h.append(image.shape[0])
        w.append(image.shape[1])
        
    d = {'h-range': [min(h), max(h)],
         'w-range': [min(w), max(w)]}
    
    return d 

def load_images(image_names, mode='train'):

    with open(PATH_PARAMETERS) as f:
        params = json.load(f)
    params = params['models_settings']

    if mode=='train':
        data_dir = params['train_dir']
    if mode=='val':
        data_dir = params['test_dir']

    resize_w = params['resize_width']
    equalize = bool(params['equalize'])
      
    images = []
    for image_name in image_names:
        
        file_name = os.path.normpath(os.path.join(data_dir, mode+params['image_folder'],  image_name))
        image = Image.open(file_name)
        
        # if resize_w is not None: 
        #     orig_w, orig_h = image.size[:2]
        #     resize_h = int(resize_w/orig_w*orig_h)
        #     image = np.array(image.resize((resize_w,resize_h), Image.BILINEAR))
            
        images.append(np.array(image))
        
    return images

def load_masks(image_names, mode='train'):
    
    with open(PATH_PARAMETERS) as f:
        params = json.load(f)
    params = params['models_settings']

    if mode=='train':
        data_dir = params['train_dir']
    if mode=='val':
        data_dir = params['test_dir']

    resize_w = params['resize_width']

    masks = []
    for image_name in image_names:  
        image_name = re.sub(".jpg", "_lab.png", image_name)
        file_name = os.path.normpath(os.path.join(data_dir, mode+params['mask_folder'],  image_name))
        mask = Image.open(file_name)
        
        # if resize_w is not None:
        #     orig_w, orig_h = mask.size[:2]
        #     resize_h = int(resize_w/orig_w*orig_h)
        #     mask = mask.resize((resize_w,resize_h), Image.NEAREST)
        
        masks.append(mask2rgb(np.array(mask)))
        
    return masks
