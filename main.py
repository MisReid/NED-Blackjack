import cv2
import numpy as np
import CameraScript
import CardFiltering
import CardClassification
import OCRClassifier
import sys

img = ''
if len(sys.argv) <= 1:
     raise Exception("Not enough args!")
elif sys.argv[1] == "-t":
    # Take image
    capturer = CameraScript.Camera_Tools()
    try:
        img = capturer.TakePhoto()
    except CameraScript.VideoCaptureException as ex:
            # implement functionality later
            raise Exception(ex.args)
elif sys.argv[1] == "-p":
     img = cv2.imread(sys.argv[2])
else:
     raise Exception("Invalid Arguments")

# Filter image
filterer = CardFiltering.FilteringTools()
img_binary = filterer.color2bin(img)
cropped_img, trimmed_img = filterer.ImgTrim(img_binary)
corner_img = filterer.grabCorner(cropped_img)

# CLassify image
# Currently only have OCR
corner_bgr = cv2.cvtColor(corner_img, cv2.COLOR_GRAY2BGR)
ocrClassifier = OCRClassifier.OCRClassifier()
output = ocrClassifier.recognizeText(corner_bgr, "crnn_cs.onnx")
print(output)