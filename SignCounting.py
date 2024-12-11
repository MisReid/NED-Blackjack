import cv2 # type: ignore
import numpy as np # type: ignore

## GOALs 
# Make something to find the right x values to count that column
# Then Make something to go down vertically and log when the pixel color changes from black to white?
    # White to Black? And stop counting when outside of contour so it doesn't count the change on the outer edge


class symbolCounter:

    #Detecting when the image changes color from White to Black at certain columns
    def WhiteToBlackDetector(image_path):
        #Image setup
        img = cv2.imread(image_path) #opening image

        ## Defining Variables
        height, width, _ = img.shape
        print("Width: {}, Height: {}.".format(width, height))
        transitions = [] #empty variable
        
        # defining dimensions
        row = range(height)
        x1 = 0.13 * width; x1 = int(x1) #Setting up our 3 columns at percentage distances across the width of the card
        x2 = 0.405 * width; x2 = int(x2)
        x3 = 0.69 * width; x3 = int(x3)
        column = [x1, x2, x3]  # Specifying the x-coordinates to check  

        #Setting the Flag
        Flag = 1  #Tracks if we are on a symbol (0 = on black, 1 = on white), 1 by default to combat the initial black to white edge shift?

        for xIndex in column:
            #print(xIndex)
            print("New Column at: ({})".format(xIndex))
            
            #going from y = 0 to y = height
            for yIndex in row:
                # Check if current pixel is white and next pixel is black
                # if y = 0 (we're on black) and we were just on white (Flag == 1): save point to transitions and change flag to 0 (on black)
                # also it indexes y, x because thats just how cv works
                if (img[yIndex,xIndex] == 0).any() and Flag == 1:
                    #to filter out the incorrect points at the top and bottom
                    if yIndex < 0.97*height and yIndex > 0.03*height:
                        transitions.append((xIndex, yIndex))
                        print("Point Appended: ({}, {})".format(xIndex, yIndex))
                        Flag = 0
                    else:
                        print("Transtition Point out of Range: ({}, {})".format(xIndex, yIndex))
                # if (img[yIndex,xIndex] == 0).any() and Flag == 1:    #old version save
                    # transitions.append((xIndex, yIndex))
                    # print("Point Appended")
                #Else if it sees black but we were already on black (Flag = 0): pass (as we're on black still)
                elif (img[yIndex,xIndex] == 0).any() and Flag == 0:
                    pass
                #else if it sees white and we were just on black: reset the flag so it can register the next symbol
                elif (img[yIndex,xIndex] == 255).any() and Flag == 0:
                    Flag = 1
                #else: we are on white
                else:
                    pass

        # Display points on the original image
        for x, y in transitions:
            cv2.circle(img, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
        
        transitionTotal = len(transitions)


        return transitions, transitionTotal, img

    def BoundingBox(image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #not needed if inputted pictures are already made B & W
        edges = cv2.Canny(gray, 100, 200)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)  # Get bounding box coordinates
            
            #removing the too small bounding rectangles
            if w < 30:
                w = 0
            if h < 30:  #30 is arbitrary
                h = 0

            #Making Final Points
            xf = x + w
            yf = y + h

            #Making them integers so they don't have decimal points attached - pixels cant be something.5, must be integer
            xf = int(xf)
            yf = int(yf)

            #Checking If they are too small, and then dont write them if so      
            if w > 0 and h > 0:
                #cv2.rectangle(image, start_point, end_point, color, thickness)
                cv2.rectangle(img, (x, y), (xf, yf), (0, 255, 0), 2)  # Draw rectangle
                
        return img
    
    def NestedContours(image_path):
        # Read the image
        img = cv2.imread(image_path) 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                    #Unneeded steps for the already trimmed images
        _, thresh = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)    #Also unneeded for trimmed, just need to update variables later
        # cv2.threshold(source, thresholdValue, maxVal, thresholdingTechnique) 

        # Find contours with hierarchy
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw all contours
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        return img


    ## OUT OF THE FUNCTIONS

    #Setting up the filepath
    directory = "C:/Users/holds/SPRBlackjackRobot/NED-Blackjack/Card_Database/Card_Outputs"
    filename = "10Spade_trm.png"
    #filename = "5Diamond.jpg"
    image_path = directory + "/" + filename

    # Getting the image with bounding boxes
    # Calcs the width (w) needed for the white_to_black checker!!!
    imgBound = BoundingBox(image_path)

    # Getting the image with Contours to print
    imgContours = NestedContours(image_path)
        
    # Getting the locations of the symbols and the image of them to display
    transitions, transitionTotal, imgW2B = WhiteToBlackDetector(image_path)
    print("Transition Points are: {}".format(transitions))

    transitionTotal = len(transitions)
    print("There are {} Transition Points.".format(transitionTotal))

    # Display the image with contours
    cv2.imshow('Changes in Color Points', imgW2B)
    #cv2.imshow('BoundingBox', imgBound)
    #cv2.imshow('Contours', imgContours)  #temporarily suppressed
    cv2.waitKey(0)
    cv2.destroyAllWindows()