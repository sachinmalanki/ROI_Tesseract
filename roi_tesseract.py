import sys
import numpy as np
import cv2
import math
from scipy import ndimage
import pytesseract
import tkinter
from tkinter import ttk
import threading

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

IMAGE_FILE_LOCATION = sys.argv[1]
#IMAGE_FILE_LOCATION = 'D:\Transcript-1.png'
print("Image location is ", IMAGE_FILE_LOCATION)
input_img = cv2.imread(IMAGE_FILE_LOCATION)
configStr = " "

# ORIENTATION CORRECTION/ADJUSTMENT

def orientation_correction(img, save_image=False):
    # GrayScale Conversion for the Canny Algorithm
    # if (img.empty()):
    # img_gray = cv2.COLOR_BGR2GRAY
    # elif (img.channels()>1):

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # else:
    # img_gray = img

    # Canny Algorithm for edge detection was developed by John F. Canny not Kennedy!! :)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    # Using Houghlines to detect lines
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    # Finding angle of lines in polar coordinates
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # Getting the median angle
    median_angle = np.median(angles)

    # Rotating the image with this median angle
    img_rotated = ndimage.rotate(img, median_angle)

    if save_image:
        cv2.imwrite('orientation_corrected.jpg', img_rotated)
    return img_rotated

img_rotated = orientation_correction(input_img)

# REGION OF INTEREST (ROI) SELECTION

# initializing the list for storing the coordinates
coordinates = []


# Defining the event listener (callback function)
def shape_selection(event, x, y, flags, param):
    # making coordinates global
    global coordinates

    # Storing the (x1,y1) coordinates when left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates = [(x, y)]

        # Storing the (x2,y2) coordinates when the left mouse button is released and make a rectangle on the selected region
    elif event == cv2.EVENT_LBUTTONUP:
        coordinates.append((x, y))

        # Drawing a rectangle around the region of interest (roi)
        cv2.rectangle(image, coordinates[0], coordinates[1], (0, 0, 255), 2)
        cv2.imshow("image", image)


def extract_roi_image():
    if len(coordinates) == 2:
        x1 = coordinates[0][0]
        y1 = coordinates[0][1]
        x2 = coordinates[1][0]
        y2 = coordinates[1][1]

        image_roi = image_copy[coordinates[0][1]:coordinates[1][1],
                    coordinates[0][0]:coordinates[1][0]]

        text = pytesseract.image_to_string(image_roi)
        print("Extracted text for the selected region is \n", text)
        keyName = input("Enter Key Name for selected region\n")
        print("Rectangle dims for key " + keyName + " are below:")
        dims = str(x1) + "-" + str(y1) + "-" + str(x2 - x1) + "-" + str(y2 - y1)
        print(dims)
        global configStr
        configStr = configStr + "<key name=\"" + keyName + "\"" + "dimensions=\"" + dims + "\"" + "></keys>\n"


# load the image, clone it, and setup the mouse callback function
image = img_rotated
image_copy = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)
cv2.imshow('image', image)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    # cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == 13:
        extract_roi_image()  # If 'enter' is pressed, apply OCR

    if key == ord("c"):  # Clear the selection when 'c' is pressed
        image = image_copy.copy()

    if key == ord("q"):
        break

docName = input("Enter Document Name\n")
fullConfig = "<document name\"" + docName + "\"" + ">\n"
fullConfig += configStr
fullConfig += "</document>"
print("Config file is \n")
print(fullConfig)

# closing all open windows
cv2.destroyAllWindows()
