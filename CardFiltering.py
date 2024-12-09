#Card Filtering.py
import os
import cv2
import numpy as np

#Paths
#img = os.path.relpath(r'./Card_Database/2Club.jpg')
Card_Database = os.path.relpath(r'./captured_image.jpg')

class FilteringTools:
    
    def color2bin(img = ''):
        img_name = img.split(".")[0]
        
        ##Mask
        #read image
        img_grey = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        img_bw = cv2.GaussianBlur(img_grey,(5,5),0)

        # define a threshold, 128 is the middle of black and white in grey scale
        thresh = 150

        # threshold the image
        img_binary = cv2.threshold(img_bw, thresh, 255, cv2.THRESH_BINARY)[1]

        return img_binary,img_name
    
    def ImgTrim(img_binary):
        
        contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(contours[0])
        x_buff = int(8.85/62.8 * w)
        y_buff = int(6.05/88.1 * h)
        
        x_new = x + x_buff
        y_new = y + y_buff
        w_new = w - x_buff
        h_new = h - y_buff
        
        fitted_image = img_binary[y : y+h , x : x+w]
        cropped_image = img_binary[y_new : y_new + h_new , x_new : x_new + w_new]

        return fitted_image , cropped_image
'''
##UNCOMMENT THIS WHEN I CAN FIGURE OUT WINDOWS FILESYSTEM PERMISSIONS
dataset = open(Card_Database)

for image in dataset:
    color_image = image
    img_name,img_binary = FilteringTools.color2bin(color_image)    
    #save image
    cv2.imwrite(f'./{img_name}_bw.png',img_binary) 
'''   

color_image = Card_Database
img_binary, img_name = FilteringTools.color2bin(color_image)
cropped_img, trimmed_img = FilteringTools.ImgTrim(img_binary)
    
#save image
cv2.imwrite(f'./{img_name}_bin.png',img_binary) 
cv2.imwrite(f'./{img_name}_crp.png',cropped_img) 
cv2.imwrite(f'./{img_name}_trm.png',trimmed_img) 
