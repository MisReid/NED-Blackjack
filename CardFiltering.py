#Card Filtering.py
from matplotlib import pyplot as plt
import os
from os import path
import cv2
import numpy as np
from math import dist
from math import acos

#Paths
Card_Database = r'./Card_Database'
Card_Outputs = r'./Card_Database/Card_Outputs'

#DEBUG BOOL
loop_through_files = True

class FilteringTools:
    
    def color2bin(img = ''):
        img_name = img.split(".")[0]
        input_img = path.join(Card_Database,img)
        ##Mask
        #read image
        img_grey = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)
        img_bw = cv2.GaussianBlur(img_grey,(5,5),0)

        # define a threshold, 128 is the middle of black and white in grey scale
        thresh = 200

        # threshold the image
        img_binary = cv2.threshold(img_bw, thresh, 255, cv2.THRESH_BINARY)[1]

        return img_binary,img_name
    
    def ImgTrim(img_binary):
        
        contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        # Finds the largest contour (card edge)
        largest = contours[0]
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > cv2.contourArea(largest):
                largest = contour

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest)
        x_buff = int(8.85/62.8 * w)
        y_buff = int(6.05/88.1 * h)
        
        x_new = x + x_buff
        y_new = y + y_buff
        w_new = w - x_buff
        h_new = h - y_buff
        
        fitted_image = img_binary[y : y+h , x : x+w]
        cropped_image = img_binary[y_new : y_new + h_new , x_new : x_new + w_new]

        return fitted_image , cropped_image

    def ImgRotate(base_img):

        contours, _ = cv2.findContours(base_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # Finds the largest contour (card edge)
        largest = contours[0]
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > cv2.contourArea(largest):
                largest = contour

        highest_y = largest[0]
        next_highest_y = [0,0]

        for point in largest:
            if point[1] > highest_y[1]:
                next_highest_y = highest_y
                highest_y = point

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest)

        (h_img, w_img) = base_img.shape[:2]
        center = (w_img // 2 , h_img // 2)

        #Define Rotation Matrix
        p0 = [x,y]  # Top Left Corner
        p1 = [w,h]  # Top Right Corner
        p2 = [w,y]  # Top Right Corner projected to x axis 
        angle = acos(dist(p2,p0),dist(p1,p0))   #angle between [p0 -> p2] and [p0 -> p1]
        scale = 1.0

        M = cv2.getRotationMatrix2D(center, angle, scale)

        rotate_img = cv2.warpAffine(base_img, M, (w_img, h_img))

        return rotate_img

if loop_through_files is True:
    counter = 1
    dataset = os.listdir(Card_Database)

    for image in dataset:

        if image == "Card_Outputs":
            pass
        else:
            #Format image
            color_image = image
            img_binary,img_name = FilteringTools.color2bin(color_image)
            rotate_img = FilteringTools.ImgRotate(img_binary)
            cropped_img, trimmed_img = FilteringTools.ImgTrim(rotate_img)  

            #save image
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_bin.png'),img_binary)
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_rot.png'),rotate_img) 
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_crp.png'),cropped_img) 
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_trm.png'),trimmed_img)
            print(f"Image outputs Written : {counter} of {len(dataset)}")
            counter += 1

else:

    color_image = Card_Database
    img_binary, img_name = FilteringTools.color2bin(color_image)
    rotate_img = FilteringTools.ImgRotate(img_binary)    
    cropped_img, trimmed_img = FilteringTools.ImgTrim(img_binary)
    
    #save image
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_bin.png'),img_binary)
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_rot.png'),rotate_img) 
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_crp.png'),cropped_img) 
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_trm.png'),trimmed_img)
    print("Image outputs Written") 
