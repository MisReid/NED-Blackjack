#CameraScript.py
import cv2

class Camera_Tools:
    
    
    
    def TakePhoto():
        # Open a connection to the webcam (0 is the default camera)
        video_capture = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not video_capture.isOpened():
            raise Exception("Could not open video device")

        # Read a frame from the webcam
        ret, frame = video_capture.read()

        # Release the webcam
        video_capture.release()

        # Check if the frame was captured successfully
        if ret:
            # Save the frame as a JPG file
            cv2.imwrite('captured_image.jpg', frame)
        else:
            print("Failed to capture image")

#Ran when script is run independently. The function should be run in another script            
Camera_Tools.TakePhoto()
