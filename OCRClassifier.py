import cv2
import numpy as np

class OCRClassifier:
    @staticmethod
    def decodeText(scores):
        text = ""
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
        # from chineseocr import alphabet
        for i in range(scores.shape[0]):
            vals = list(scores[i][0])
            cont = True
            while (cont):
                c = np.argmax(vals)
                if c == 0 :   
                    text += '-'
                    cont = False
                elif (c < 11) or c == 20 or c == 21 or c == 27 :
                    text += alphabet[c - 1]
                    cont = False
                else :
                    vals[c] = -10000

        # adjacent same letters as well as background text must be removed to get the final output
        char_list = []
        for i in range(len(text)):
            if text[i] != '-' and (not (i > 0 and text[i] == text[i - 1])):
                char_list.append(text[i])
        return ''.join(char_list)

    def recognizeText(self, img, ocr_path):
        ocr = cv2.dnn.readNet(ocr_path)
        blob = cv2.dnn.blobFromImage(img, size=(100, 32) , mean=127.5, scalefactor=(1/127.5))
        ocr.setInput(blob)
        result = ocr.forward()
        ret = self.decodeText(result)
        return ret
    
if __name__ == "__main__":
    img = cv2.imread("10Club_cor.png")
    classifier = OCRClassifier()
    ret = classifier.recognizeText(img, "crnn_cs.onnx")
    print(ret)