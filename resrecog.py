import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

boundaries = [
	([90, 80, 60], [150, 140, 130]),
	([80, 25, 0], [220, 95, 60]),
	([25, 140, 180], [75, 180, 250]),
	([10, 10, 100], [60, 60, 200])
]

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])



# keep looping
while True:
	# grab the current frame
    (grabbed, frame) = camera.read()
    #Create a black version of given image as background
    black = [0,0,0]
    blacknp = np.array(black, dtype = "uint8")
    blackmask = cv2.inRange(frame, blacknp, blacknp)
    filtered = cv2.bitwise_and(frame,frame,mask=blackmask)
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
    if args.get("video") and not grabbed:
		break

    #yooloo
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

    #Show result and wait for user to close window
    cv2.imshow("video", np.hstack([filtered,frame]))
    key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
