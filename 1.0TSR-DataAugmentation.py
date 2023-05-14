from msilib.schema import Icon
from PIL import Image
import numpy as np
import os
import cv2
from PIL import Image, ImageStat, ImageEnhance
import random

labels = ['pl', 'p6', 'ph', 'w', 'pa', 'p27', 'i5', 'p1', 'il', 'p5', 'pm', 'p19', 'ip', 'p11', 'p13', 
              'p26', 'i2', 'pn', 'p10', 'p23', 'pbp', 'p3', 'p12', 'pne', 'i4', 'pb', 'pg', 'pr']
#labels is same with the data YAML file’s name setction.

global img

icon_name = 'pm' #icon_name is the name of the class that you want to Augment. Here is the example "pm", choose from the labels [].
label_num = labels.index(icon_name)
label_num = str(label_num)

icon = Image.open("/marks/%s.png" % icon_name) #The path that you store the marks.
icon_w,icon_h = icon.size
icon_w = int(icon_w)
icon_h = int(icon_h)
icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
r, g, b, a = icon.split()

img_folder = ("/images") #The path that you store the images which need to be augmentated.
img_list = os.listdir(img_folder)
img_list.sort()


label_folder = ("/labels") #The path that you store the images' label files(.txt) .
label_list = os.listdir(label_folder)
label_list.sort()

def xywh2xyxy(x, w1, h1, img):
    global icon_w
    global icon_h
    global top_left_x
    global top_left_y
    global bottom_right_x
    global bottom_right_y
    label, x, y, w, h = x

    x_t = x * w1
    y_t = y * h1
    w_t = w * w1
    h_t = h * h1

    # Calculated coordinates
    top_left_x = x_t - w_t / 2
    top_left_y = y_t - h_t / 2
    bottom_right_x = x_t + w_t / 2
    bottom_right_y = y_t + h_t / 2
    top_left_y = int(top_left_y)
    top_left_x = int(top_left_x)
    bottom_right_x = int(bottom_right_x)
    bottom_right_y = int(bottom_right_y)

    print('class:{}'.format(labels[int(label)]))
    print("left_top_x:{}".format(top_left_x))
    print("top_left_y:{}".format(top_left_y))
    print("bottom_right_x:{}".format(bottom_right_x))
    print("bottom_right_y:{}".format(bottom_right_y))
    icon_w = bottom_right_x-top_left_x
    icon_h = bottom_right_y-top_left_y

    print(icon_w,icon_h)

if __name__ == '__main__':
    num = 0
    for i in range(len(img_list)):
        image_path = img_folder + "/" + img_list[i]
        label_path = label_folder + "/" + label_list[i]
        print(img_list[i])
        # load the image that need to be augmentated
        img = Image.open(str(image_path))
        img = img.convert("RGBA") 
        w, h = img.size 
        # read label file
        with open(label_path, 'r') as f:
            lb = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)
        # every line in the label file
        for x in lb:
            img = xywh2xyxy(x, w, h, img)
            icon_w = int(icon_w)
            icon_h = int(icon_h)
            icon = Image.open("marks/%s.png" % icon_name) #The root you store the marks.
            brightness_factor = random.uniform(1, 0.5)
            #print (brightness_factor)
            enhancer = ImageEnhance.Brightness(icon)
            icon = enhancer.enhance(brightness_factor)
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
            r, g, b, a = icon.split()
            img = Image.open(str(image_path))
            img = img.convert("RGBA") 
            img.paste(icon, (top_left_x,top_left_y,bottom_right_x,bottom_right_y), mask = a)
            # save augmentated image
            img=img.convert('RGB')
            img.save(str(image_path)) #replace the original image
    #Rewrite label files
    num = len(label_list)
    list = range(num) #Create a list of integers from 0 to num 
    for i in list: #Iterate over each file
        name = label_list[i]
        readfile = open(label_folder+"/"+name, 'r') 
        fline = readfile.readlines() 
        savetxt = open(label_folder+"/"+name,'w+')
        for temp in fline: #Iterate over each line
            #print(type(temp)) 
            list1=temp.split()
            print(list1)
            list1[0] = label_num
            b = " ".join(list1)  
            savetxt.write(b) 
            savetxt.write('\n')

        
        
       


