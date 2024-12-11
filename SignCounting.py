import cv2 # type: ignore
import numpy as np # type: ignore
import CardClassification as classify


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
        x1 = 0.14 * width; x1 = int(x1) #Setting up our 3 columns at percentage distances across the width of the card
        x2 = 0.41 * width; x2 = int(x2)
        x3 = 0.695 * width; x3 = int(x3)
        column = [x1, x2, x3]  # Specifying the x-coordinates to check  

        #Setting the Flag
        Flag = 1  #Tracks if we are on a symbol (0 = on black, 1 = on white), 1 by default to combat the initial black to white edge shift?

        for xIndex in column:
            #print(xIndex)
            print("New Column at: ({})".format(xIndex))
            prevPoint = 0
            #going from y = 0 to y = height
            for yIndex in row:
                # Check if current pixel is white and next pixel is black
                # if y = 0 (we're on black) and we were just on white (Flag == 1): save point to transitions and change flag to 0 (on black)
                # also it indexes y, x because thats just how cv works
                if (img[yIndex,xIndex] == 0).any() and Flag == 1:
                    #to filter out the incorrect points at the top and bottom (lower 10% and top 2%)
                    if yIndex < 0.9*height and yIndex > 0.02*height:
                        #Giving it a minimum distance it needs to travel to log another point
                        if (yIndex - prevPoint > 0.21 * height) or prevPoint == 0:
                            prevPoint = yIndex
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


    ## OUT OF THE FUNCTION

    #Setting up the filepath
    directory = "C:/Users/holds/SPRBlackjackRobot/NED-Blackjack/Card_Database/Card_Outputs"
    filename = "AceSpade_trm.png"
    image_path = directory + "/" + filename
        
    # Getting the locations of the symbols and the image of them to display
    transitions, transitionTotal, imgW2B = WhiteToBlackDetector(image_path)
    print("Transition Points are: {}".format(transitions))
    print("There are {} Transition Points.".format(transitionTotal))

    print("Card Score: {}".format(classify.ClassificatonTools.card_scoring(transitionTotal)))

    # Display the image with transition points marked
    cv2.imshow('Changes in Color Points', imgW2B)
    cv2.waitKey(0)
    cv2.destroyAllWindows()