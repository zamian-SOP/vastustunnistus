#Import necessary packages
import numpy as np
import argparse
import imutils
import cv2

#Create argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="Path to optional video file.")
args = vars(ap.parse_args())

#Define list of boundaries to parse through
boundaries = [
	([0, 0, 100], [75, 75, 250]),
	([100, 100, 0], [250, 250, 75]),
	([100, 0, 0], [250, 75, 75]),
	([0, 100, 0], [75, 250, 75])
]

#Grab webcam if no video file, else take video file
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
else:
	camera = cv2.VideoCapture(args["video"])



#Loop until manually broken or given video file ends
while True:
	#Grab the current frame
    (grabbed, frame) = camera.read()
    #Create a black version of grabbed frame as background
    black = [0,0,0]
    blacknp = np.array(black, dtype = "uint8")
    blackmask = cv2.inRange(frame, blacknp, blacknp)
    filtered = cv2.bitwise_and(frame,frame,mask=blackmask)
	#If a video was given and no frame grabbed, the video has ended
    if args.get("video") and not grabbed:
		break

    #Loop through the boundaries in the frame
    for (lower, upper) in boundaries:
    	#Make numpy arrays out of boundaries
    	lower = np.array(lower, dtype = "uint8")
    	upper = np.array(upper, dtype = "uint8")
    	#Create mast using lower and upper boundaries
    	mask = cv2.inRange(frame, lower, upper)
    	#Apply mask to image
    	output = cv2.bitwise_and(frame, frame, mask = mask)
    	#Add the filtered color to final image
    	filtered = cv2.addWeighted(filtered,1, output,1, 0)

    #Show resulting frame
    cv2.imshow("Video", np.hstack([filtered,frame]))
    key = cv2.waitKey(1) & 0xFF
	#Stop looping if "q" is pressed
    if key == ord("q"):
        break

#Close open windows and camera as the program ends
camera.release()
cv2.destroyAllWindows()
