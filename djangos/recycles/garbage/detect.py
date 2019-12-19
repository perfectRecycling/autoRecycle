from __future__ import division

from .models import *
from .utils.utils import *
from .utils.datasets import *

import os
import sys
import time
import datetime
import argparse

from PIL import Image, ExifTags

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable
import torch.nn.functional as F

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator
from torchvision.utils import save_image
import shutil

def pad_to_square(img, pad_value):
    c, h, w = img.shape
    dim_diff = np.abs(h - w)
    # (upper / left) padding and (lower / right) padding
    pad1, pad2 = dim_diff // 2, dim_diff - dim_diff // 2
    # Determine padding
    pad = (0, 0, pad1, pad2) if h <= w else (pad1, pad2, 0, 0)
    # Add padding
    img = F.pad(img, pad, "constant", value=pad_value)

    return img, pad

def resize(image, size):
    image = F.interpolate(image.unsqueeze(0), size=size, mode="nearest").squeeze(0)
    return image

class parser:
    def __init__(self):
        self.image_folder = 'recycles/garbage/data/garbage/samples'
        self.model_def = 'recycles/garbage/config/yolov3-garbage.cfg'
        self.weights_path = 'recycles/garbage/checkpoints/jonghyun.pth'
        #self.weights_path = 'recycles/garbage/checkpoints/jonghyun.pth'
        self.class_path = 'recycles/garbage/data/garbage/garbage.names'
        self.conf_thres = 0.9
        self.nms_thres = 0.6
        self.batch_size = 1
        self.n_cpu = 0
        self.img_size = 416

opt = parser()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Darknet(opt.model_def, img_size=opt.img_size).to(device)

if opt.weights_path.endswith(".weights"):
    model.load_darknet_weights(opt.weights_path)
else:
    model.load_state_dict(torch.load(opt.weights_path))

def get_model():
    return model

def recycle(model, image_path):
    model.eval()

    transform = transforms.Compose([transforms.ToTensor()])
    img = Image.open(image_path)
    img = transform(img)
    img, _ = pad_to_square(img,0)
    img = resize(img, opt.img_size)
    img = torch.unsqueeze(img, 0)
    print(image_path)
    classes = load_classes(opt.class_path)  # Extracts class labels from file

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    imgs = []  # Stores image paths
    img_detections = []  # Stores detections for each image index

    print("\nPerforming object detection:")
    prev_time = time.time()

    # Configure input
    input_imgs = Variable(img.type(Tensor))
    #save_image(input_imgs, 'img.png')

    # Get detections
    with torch.no_grad():
        detections = model(input_imgs)
        detections = non_max_suppression(detections, opt.conf_thres, opt.nms_thres)

    print(detections)

    # Log progress
    current_time = time.time()
    inference_time = datetime.timedelta(seconds=current_time - prev_time)
    prev_time = current_time
    print("\t+ Inference Time: %s" % (inference_time))

    # Save image and detections
    imgs.append(image_path)
    img_detections.extend(detections)

    # Bounding-box colors
    cmap = plt.get_cmap("tab20b")
    colors = [cmap(i) for i in np.linspace(0, 1, 20)]

    #print(imgs)

    print("\nSaving images:")
    # Iterate through images and save plot of detections
    for img_i, (path, detections) in enumerate(zip(imgs, img_detections)):

        print("(%d) Image: '%s'" % (img_i, path))

        # Create plot
        img = Image.open(path)
        #img = img.resize((opt.img_size, opt.img_size))
        img = np.array(img)
        #print(img.shape)
        plt.figure()
        fig, ax = plt.subplots(1)
        ax.imshow(img)

        returns = []
        dates = []
        filenames = []
        # Draw bounding boxes and labels of detections
        if detections is not None:
            # Rescale boxes to original image
            detections = rescale_boxes(detections, opt.img_size, img.shape[:2])
            #print(detections)
            unique_labels = detections[:, -1].cpu().unique()
            n_cls_preds = len(unique_labels)
            bbox_colors = random.sample(colors, n_cls_preds)
            count = 0
            for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:

                print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf.item()))

                box_w = x2 - x1
                box_h = y2 - y1

                color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]
                # Create a Rectangle patch
                bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor="none")
                # Add the bbox to the plot
                ax.add_patch(bbox)
                # Add label
                plt.text(
                    x1,
                    y1,
                    s=str(count)+':'+classes[int(cls_pred)]+':'+str(round(cls_conf.item(), 4)),
                    color="white",
                    verticalalignment="top",
                    bbox={"color": color, "pad": 0},
                )
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                returns.append(classes[int(cls_pred)])
                dates.append(date)
                count = count + 1

        # Save generated image with detections
        plt.axis("off")
        plt.gca().xaxis.set_major_locator(NullLocator())
        plt.gca().yaxis.set_major_locator(NullLocator())

        first_image = ''
        for i,date in enumerate(dates):

            if i == 0:
                folder = date.split(' ')[0]
                folder = 'recycles/image_results/'+folder

                if not(os.path.isdir(folder)):
                    os.makedirs(os.path.join(folder))

                filename = returns[i]+'_'+dates[i]+'_'+str(i).zfill(5)
                first_image = folder+'/'+filename+'.jpg'
                filenames.append(folder+'/'+filename+'.jpg')
                plt.savefig(f"{folder}/{filename}.jpg", bbox_inches="tight", pad_inches=0.0)
                plt.close()

            else:

                folder = date.split(' ')[0]
                folder = 'recycles/image_results/'+folder

                if not(os.path.isdir(folder)):
                    os.makedirs(os.path.join(folder))

                filename = returns[i]+'_'+dates[i]+'_'+str(i).zfill(5)
                filenames.append(folder+'/'+filename+'.jpg')
                shutil.copy2(first_image,folder+'/'+filename+'.jpg')
    return returns, dates, filenames
