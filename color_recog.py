#Import necessary packages
import numpy as np
import argparse
import cv2

#Create argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

#Read image
image = cv2.imread(args["image"])

#Create list of boundaries
boundaries = [
	([90, 80, 60], [150, 140, 130]),
	([80, 25, 0], [220, 95, 60]),
	([25, 140, 180], [75, 180, 250]),
	([10, 10, 100], [60, 60, 200])
]

#Create a black version of given image as background
black = [0,0,0]
blacknp = np.array(black, dtype = "uint8")
blackmask = cv2.inRange(image, blacknp, blacknp)
filtered = cv2.bitwise_and(image,image,mask=blackmask)

#Loop through boundaries
for (lower, upper) in boundaries:
	#Make numpy arrays out of boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
	#Create mast using lower and upper boundaries
	mask = cv2.inRange(image, lower, upper)
	#Apply mask to image
	output = cv2.bitwise_and(image, image, mask = mask)
	#Add the filtered color to final image
	filtered = cv2.addWeighted(filtered,1, output,1, 0)

#Show result and wait for user to close window
cv2.imshow("images", np.hstack([filtered,image]))
cv2.waitKey(0)
