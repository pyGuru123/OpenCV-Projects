# pip install opencv-python
# pip install opencv-contrib-python
# pip install pillow

import cv2
import numpy as np
from PIL import Image, ImageTk

class ColorTracker:
	def __init__(self, file):
		self.image_orig = cv2.imread(file)
		self.image = cv2.cvtColor(self.image_orig, cv2.COLOR_BGR2RGB)

		self.img = cv2.resize(self.image_orig, (450,400))
		self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

	def display_original_image(self, size):
		tkimg = cv2.resize(self.image, size)
		tkimg = Image.fromarray(tkimg)
		tkimg = ImageTk.PhotoImage(tkimg)

		return tkimg

	def detect_from_hsv(self, arr1, arr2):
		lower = np.array(arr1)
		upper = np.array(arr2)
		mask = cv2.inRange(self.hsv, lower, upper)

		detected = cv2.bitwise_and(self.img, self.img, mask=mask)
		detected = cv2.cvtColor(detected, cv2.COLOR_HSV2RGB)
		tkimg = Image.fromarray(detected)
		tkimg = ImageTk.PhotoImage(tkimg)

		return tkimg