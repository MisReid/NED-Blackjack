import cv2
import numpy as np
import CameraScript
import CardFiltering
import CardClassification
import OCRClassifier
import sys

def main(img):
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
    return output

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
    out = main(img)
    print(out)
elif sys.argv[1] == "-p":
     img = cv2.imread(sys.argv[2])
     out = main(img)
     print(out)
elif sys.argv[1] == "-a":
    suits = ["Club", "Diamond", "Heart", "Spade"]
    file = open("data.csv", 'w')
    file.write("Suit, Rank, Output\n")
    for i in range(1, 14):
        rank = ""
        match i:
            case 1:
                 rank = "Ace"
            case 11:
                rank = "J"
            case 12:
                rank = "Q"
            case 13:
                rank = "K"
            case _:
                rank = f"{i}"
        for suit in suits:
            img = cv2.imread(f"Card_Database/{rank}{suit}.jpg")
            out = main(img)
            file.write(f"{suit}, {rank}, {out}\n")
else:
     raise Exception("Invalid Arguments")