#CameraScript.py
import cv2

'''Handler file for the camera. Place any camera or device operation functions here'''
class Camera_Tools:
       
    def TakePhoto():
        # Open webcam(default camera = 0)
        video_capture = cv2.VideoCapture(6)

        if not video_capture.isOpened():
            raise Exception("Could not open video device")

        # Read a frame from the webcam and release
        ret, frame = video_capture.read()
        video_capture.release()

        # Check if the frame was captured successfully
        if ret:
            cv2.imwrite('captured_image.jpg', frame)                # Save the frame as a JPG file
            
        else:
            print("Failed to capture image")
        
        return 

#Ran when script is run independently. The function should be run in another script            
Camera_Tools.TakePhoto()
