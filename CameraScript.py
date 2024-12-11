#CameraScript.py
import cv2

class VideoCaptureException(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        if error_code == 1 :
            message = "Could not open video device"
        elif error_code == 2 :
            message = "Failed to capture image"
        else :
            message = "Unkown Issue"
        super().__init__(message)
            

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

class Camera_Tools:
    
    def TakePhoto(should_write):
        # Open a connection to the webcam (0 is the default camera (webcam))
        # (1 is the default for windows?)
        # (2 is the default for the ubuntu laptop)
        video_capture = cv2.VideoCapture(1)

        # Check if the webcam is opened correctly
        if not video_capture.isOpened():
            raise VideoCaptureException(1)

        # Read a frame from the webcam
        ret, frame = video_capture.read()

        # Release the webcam
        video_capture.release()

        # Check if the frame was captured successfully
        if ret:
            if (should_write):
                # Save the frame as a JPG file
                cv2.imwrite('captured_image.jpg', frame)
            return frame
        else:
            raise VideoCaptureException(2)
            
if __name__=="__main__":   
    Camera_Tools.TakePhoto(True)
