from msilib.schema import Icon
from PIL import Image
import numpy as np
import os
import cv2
from PIL import Image, ImageStat, ImageEnhance
import random

labels = ['pl80', 'p6', 'ph', 'w', 'pa', 'p27', 'i5', 'p1', 'il70', 'p5', 'pm', 'p19', 'ip', 'p11', 'p13', 'p26', 'i2', 'pn', 'p10', 'p23', 'pbp', 'p3', 'p12', 
          'pne', 'i4', 'pb', 'pg', 'pr','pl5','pl10', 'pl15','pl20','pl25','pl30','pl35','pl40','pl50','pl60','pl65','pl70','pl90','pl100','pl110',
          'pl120','il50','il60','il80','il90','il100','il110']
global img

count = 0
il_number = 0

img_folder = ("C:/Users/JingZ/source/repos/tt100k_2021/pg_val2/images")
img_list = os.listdir(img_folder)
img_list.sort()

label_folder = ("C:/Users/JingZ/source/repos/tt100k_2021/pg_val2/labels")
label_list = os.listdir(label_folder)
label_list.sort()

def xywh2xyxy(x, w1, h1, img):
    global icon_w
    global icon_h
    global top_left_x
    global top_left_y
    global bottom_right_x
    global bottom_right_y
    global label
    label, x, y, w, h = x
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    # print("原图宽高:\nw1={}\nh1={}".format(w1, h1))
    # 边界框反归一化
    x_t = x * w1
    y_t = y * h1
    w_t = w * w1
    h_t = h * h1
    # print("反归一化后输出：\n第一个:{}\t第二个:{}\t第三个:{}\t第四个:{}\t\n\n".format(x_t, y_t, w_t, h_t))
    # 计算坐标
    top_left_x = x_t - w_t / 2
    top_left_y = y_t - h_t / 2
    bottom_right_x = x_t + w_t / 2
    bottom_right_y = y_t + h_t / 2
    top_left_y = int(top_left_y)
    top_left_x = int(top_left_x)
    bottom_right_x = int(bottom_right_x)
    bottom_right_y = int(bottom_right_y)

    print('标签:{}'.format(labels[int(label)]))
    print("左上x坐标:{}".format(top_left_x))
    print("左上y坐标:{}".format(top_left_y))
    print("右下x坐标:{}".format(bottom_right_x))
    print("右下y坐标:{}".format(bottom_right_y))
    icon_w = bottom_right_x-top_left_x
    icon_h = bottom_right_y-top_left_y

    print(icon_w,icon_h)

def changepicture(icon_name, icon_w, icon_h):
    label_num = labels.index(icon_name)
    label_num = str(label_num)  
    icon_w = int(icon_w)
    icon_h = int(icon_h)
    icon = Image.open("C:/Users/JingZ/source/repos/tt100k_2021/marks/%s.png" % icon_name)
    brightness_factor = random.uniform(1, 0.7)
    #print (brightness_factor)
    enhancer = ImageEnhance.Brightness(icon)
    icon = enhancer.enhance(brightness_factor)
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    r, g, b, a = icon.split()
    img = Image.open(str(image_path))
    img = img.convert("RGBA") 
    img.paste(icon, (top_left_x,top_left_y,bottom_right_x,bottom_right_y), mask = a)
    # 保存图片
    img=img.convert('RGB')
    img.save(str(image_path))#合成后的图片路径以及文件名

def changepicture_il(icon_name, icon_w, icon_h):
    label_num = labels.index(icon_name)
    label_num = str(label_num)  
    icon_w = int(icon_w)
    icon_h = int(icon_h)
    icon = Image.open("C:/Users/JingZ/source/repos/tt100k_2021/marks/%s.png" % icon_name)
    brightness_factor = random.uniform(1.2, 0.9)
    #print (brightness_factor)
    enhancer = ImageEnhance.Brightness(icon)
    icon = enhancer.enhance(brightness_factor)
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    r, g, b, a = icon.split()
    img = Image.open(str(image_path))
    img = img.convert("RGBA") 
    img.paste(icon, (top_left_x,top_left_y,bottom_right_x,bottom_right_y), mask = a)
    # 保存图片
    img=img.convert('RGB')
    img.save(str(image_path))#合成后的图片路径以及文件名
    


if __name__ == '__main__':
    num = 0
    num = len(label_list)
    list = range(num) #创建从0到num的整数列表
    for i in range(len(img_list)):
        image_path = img_folder + "/" + img_list[i]
        label_path = label_folder + "/" + label_list[i]
        print(img_list[i])
        # 读取图像文件
        img = Image.open(str(image_path))
        img = img.convert("RGBA") 
        w, h = img.size 
        # 读取 labels
        with open(label_path, 'r') as f:
            lb = np.array([x.split() for x in f.read().strip().splitlines()])
            print(lb)
        with open(label_path, 'r') as f:
            lb2 = np.array([y.split() for y in f.read().strip().splitlines()])
            print(lb2)
        # 每一个目标
        for x in lb:
            # 反归一化并得到左上和右下坐标
            img = xywh2xyxy(x, w, h, img)
            lb[count][0] = int(x[0])
            if x[0] == '0': 
                for y in lb2:
                    if y[0] == '8':
                        il_number = il_number+1
                if il_number>0:
                    #print("highspeed%s",img_list[i])
                    pl = ['pl80','pl90','pl100','pl110','pl120']
                    #pl = ['pl80','pl90','pl100','pl110','pl120','pb']
                else:
                    pl = ['pl5','pl10', 'pl15','pl20','pl25','pl30','pl35','pl40','pl50','pl60','pl65','pl70']
                    #pl = ['pl10', 'pl15','pl20','pl25','pl35','pl65','pl70']
                il_number = 0
                icon_name = random.choice(pl)
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)
            
            elif x[0] == '1': 
                icon_name = 'p6'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '5': 
                icon_name = 'p27'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)   

            elif x[0] == '6': 
                icon_name = 'i5'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '7': 
                icon_name = 'p1'
                label_num = labels.index(icon_name)
                label_num = str(label_num)  
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '8': 
                il = ['il50','il60','il70','il80','il90','il100','il110']
                #il = ['il50','il60','il70','il80','il90','il100','il110','pb']
                icon_name = random.choice(il)
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture_il(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '9': 
                icon_name = 'p5'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '11': 
                icon_name = 'p19'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '12': 
                icon_name = 'ip'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '13': 
                icon_name =  'p11'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '14': 
                icon_name = 'p13'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '15': 
                icon_name = 'p26'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)

            elif x[0] == '16': 
                icon_name = 'i2'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)      

            elif x[0] == '17': 
                icon_name = 'pn'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)   

            elif x[0] == '18': 
                icon_name = 'p10'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num)      

            elif x[0] == '19': 
                icon_name = 'p23'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 

            elif x[0] == '20': 
                icon_name = 'pbp'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 

            elif x[0] == '21': 
                icon_name = 'p3'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 

            elif x[0] == '22': 
                icon_name = 'p12'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 

            elif x[0] == '23': 
                icon_name = 'pne'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 
                
            elif x[0] == '24': 
                icon_name = 'i4'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 

            elif x[0] == '25': 
                icon_name = 'pb'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 

            elif x[0] == '26': 
                icon_name = 'pg'
                label_num = labels.index(icon_name)
                label_num = str(label_num)               
                changepicture(icon_name, icon_w, icon_h)
                lb[count][0] = int(label_num) 
            else:
                print(x)
        
            count = count+1

        count = 0
        print(lb)
        np.savetxt(label_path, np.c_[lb], fmt='%s')



 
        
        
       


