#Card Filtering.py
from matplotlib import pyplot as plt
import os
from os import path
import cv2
import numpy as np

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
        
        debug = False
        contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        if debug is True:
            cv2.drawContours(img_binary, contours, -1, (0,255,0), 3)
            plt.imshow('Contours', contours)
            cv2.waitKey(0)
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
            cropped_img, trimmed_img = FilteringTools.ImgTrim(img_binary)  

            #save image
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_bin.png'),img_binary) 
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_crp.png'),cropped_img) 
            cv2.imwrite(path.join(Card_Outputs,f'{img_name}_trm.png'),trimmed_img)
            print(f"Image outputs Written : {counter} of {len(dataset)}")
            counter += 1

else:

    color_image = Card_Database
    img_binary, img_name = FilteringTools.color2bin(color_image)
    cropped_img, trimmed_img = FilteringTools.ImgTrim(img_binary)
    
    #save image
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_bin.png'),img_binary) 
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_crp.png'),cropped_img) 
    cv2.imwrite(path.join(Card_Outputs,f'{img_name}_trm.png'),trimmed_img)
    print("Image outputs Written") 
