
import tkinter as tk
from tkinter import *
import random
import pprint
import cv2
from PIL import Image, ImageTk
import math
import csv

import os
import numpy as np

import glob


class BoundingBoxFineTuner :

    """ Precisely finetune bounding boxes """

    def __init__(self, window, displayWidth=400, displayHeight=400, bboxIncrement=0.01) :
        """
        <window> : The Tkinter window where the map should be displayed
        <displayWidth> : Width of the display
        <displayHeight> : Height of the display
        """
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        self.bboxIncrement = bboxIncrement

        # Blanck canvas
        self.canvas = Canvas(self.frame, width=self.displayWidth, height=self.displayHeight)
        self.canvas.create_rectangle(1, 1, self.displayWidth, self.displayHeight)
        self.canvas.focus()

        self.canvas.bind("<Left>", self.lengthenBboxHorizontally)
        self.canvas.bind("<Right>", self.shortenBboxHorizontally)
        self.canvas.bind("<Down>", self.lengthenBboxVertically)
        self.canvas.bind("<Up>", self.shortenBboxVertically)

        self.canvas.bind("<d>", self.moveBboxLeft)
        self.canvas.bind("<D>", self.moveBboxLeft)
        self.canvas.bind("<q>", self.moveBboxRight)
        self.canvas.bind("<Q>", self.moveBboxRight)
        self.canvas.bind("<s>", self.moveBboxUp)
        self.canvas.bind("<S>", self.moveBboxUp)
        self.canvas.bind("<z>", self.moveBboxDown)
        self.canvas.bind("<Z>", self.moveBboxDown)

        self.canvas.focus_set() # How does this interract with other stuff ?

        self.imagePath = None
        self.bbox = None

        self.canvas.pack(pady=10)

        self.imagePath = "/home/nicolas/labellingTool/data/aaJPGlabel.jpeg"
        self.bbox = {
            "left_percentage": 0.23452768729641693,
            "top_percentage": 0.21009771986970685,
            "right_percentage": 0.30944625407166126,
            "bottom_percentage": 0.2899022801302932,
            "category": {
                "name": "Yellow",
                "color_rgb": [
                    255,
                    255,
                    0
                ]
            }
        }


    def updateImage(self) :
        try :
            self.image = cv2.imread(self.imagePath)
        except :
            print(f"[Warning] : Cannot read image '{imagePath}'")
            return

        imageHeight, imageWidth, n_channels = self.image.shape

        horizontalRange = self.bbox["right_percentage"] - self.bbox["left_percentage"]
        verticalRange = self.bbox["bottom_percentage"] - self.bbox["top_percentage"]

        imageLeftPercentage = max(0, self.bbox["left_percentage"] - 0.1 * horizontalRange)
        imageRightPercentage = min(1, self.bbox["right_percentage"] + 0.1 * horizontalRange)
        imageBottomPercentage = min(1, self.bbox["bottom_percentage"] + 0.1 * verticalRange)
        imageTopPercentage = max(0, self.bbox["top_percentage"] - 0.1 * verticalRange)

        imageLeftPixel = int(imageLeftPercentage * imageWidth)
        imageRightPixel = int(imageRightPercentage * imageWidth)
        imageBottomPixel = int(imageBottomPercentage * imageHeight)
        imageTopPixel = int(imageTopPercentage * imageHeight)

        self.image = self.image[imageTopPixel:imageBottomPixel, imageLeftPixel:imageRightPixel]
        self.image = cv2.resize(self.image, [self.displayWidth-2, self.displayHeight-2], interpolation = cv2.INTER_AREA)

        # Display image at proper position
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.image))
        self.view = self.canvas.create_image(2, 2, anchor="nw", image=self.image)

        # BBox
        def updateProp(proportion, minProportion, maxProportion) :
            newProp = (proportion - minProportion) / (maxProportion - minProportion)
            return max(min(newProp, 1), 0)

        bboxLeftPixel_onScreen = int(1 + (self.displayWidth - 2) * updateProp(self.bbox["left_percentage"], imageLeftPercentage, imageRightPercentage))
        bboxRightPixel_onScreen = int((self.displayWidth - 2) * updateProp(self.bbox["right_percentage"], imageLeftPercentage, imageRightPercentage))
        bboxBottomPixel_onScreen = int((self.displayHeight - 2) * updateProp(self.bbox["bottom_percentage"], imageTopPercentage, imageBottomPercentage))
        bboxTopPixel_onScreen = int(1 + (self.displayHeight - 2) * updateProp(self.bbox["top_percentage"], imageTopPercentage, imageBottomPercentage))

        self.canvas.create_rectangle(bboxLeftPixel_onScreen, bboxTopPixel_onScreen, bboxRightPixel_onScreen, bboxBottomPixel_onScreen, width=3)
        self.canvas.create_rectangle(bboxLeftPixel_onScreen, bboxTopPixel_onScreen, bboxRightPixel_onScreen, bboxBottomPixel_onScreen, outline="#%02x%02x%02x" % tuple(self.bbox["category"]['color_rgb']))


    def shortenBboxHorizontally(self, event=None) :
        bboxHorizontalRange = self.bbox["right_percentage"] - self.bbox["left_percentage"]
        self.bbox["right_percentage"] -= max(0, self.bboxIncrement * bboxHorizontalRange)
        self.bbox["left_percentage"] += min(1, self.bboxIncrement * bboxHorizontalRange)
        self.updateImage()

    def lengthenBboxHorizontally(self, event=None) :
        bboxHorizontalRange = self.bbox["right_percentage"] - self.bbox["left_percentage"]
        self.bbox["right_percentage"] += min(1, self.bboxIncrement * bboxHorizontalRange)
        self.bbox["left_percentage"] -= max(0, self.bboxIncrement * bboxHorizontalRange)
        self.updateImage()

    def shortenBboxVertically(self, event=None) :
        bboxVerticalRange = self.bbox["bottom_percentage"] - self.bbox["top_percentage"]
        self.bbox["top_percentage"] += min(1, self.bboxIncrement * bboxVerticalRange)
        self.bbox["bottom_percentage"] -= max(0, self.bboxIncrement * bboxVerticalRange)
        self.updateImage()

    def lengthenBboxVertically(self, event=None) :
        bboxVerticalRange = self.bbox["bottom_percentage"] - self.bbox["top_percentage"]
        self.bbox["top_percentage"] -= max(0, self.bboxIncrement * bboxVerticalRange)
        self.bbox["bottom_percentage"] += min(1, self.bboxIncrement * bboxVerticalRange)
        self.updateImage()

    def moveBboxUp(self, event=None) :
        bboxVerticalRange = self.bbox["bottom_percentage"] - self.bbox["top_percentage"]
        self.bbox["top_percentage"] -= max(0, self.bboxIncrement * bboxVerticalRange)
        self.bbox["bottom_percentage"] -= max(0, self.bboxIncrement * bboxVerticalRange)
        self.updateImage()

    def moveBboxDown(self, event=None) :
        bboxVerticalRange = self.bbox["bottom_percentage"] - self.bbox["top_percentage"]
        self.bbox["top_percentage"] += min(1, self.bboxIncrement * bboxVerticalRange)
        self.bbox["bottom_percentage"] += min(1, self.bboxIncrement * bboxVerticalRange)
        self.updateImage()

    def moveBboxLeft(self, event=None) :
        bboxHorizontalRange = self.bbox["right_percentage"] - self.bbox["left_percentage"]
        self.bbox["right_percentage"] -= max(0, self.bboxIncrement * bboxHorizontalRange)
        self.bbox["left_percentage"] -= max(0, self.bboxIncrement * bboxHorizontalRange)
        self.updateImage()

    def moveBboxRight(self, event=None) :
        bboxHorizontalRange = self.bbox["right_percentage"] - self.bbox["left_percentage"]
        self.bbox["right_percentage"] += min(1, self.bboxIncrement * bboxHorizontalRange)
        self.bbox["left_percentage"] += min(1, self.bboxIncrement * bboxHorizontalRange)
        self.updateImage()



if __name__ == "__main__" :

    window = tk.Tk()
    window.title("BBoxFineTuner")
    window.geometry('1300x800')

    bboxTuner = BoundingBoxFineTuner(window)
    bboxTuner.frame.place(x=40, y=50)


    bboxTuner.updateImage()

    exitButton = tk.Button(window, text='close window', width=10, command=window.destroy)
    exitButton.pack()

    window.mainloop()
