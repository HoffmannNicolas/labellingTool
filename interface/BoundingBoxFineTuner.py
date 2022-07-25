
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

from CategoryManager import CategoryManager, testCategoryManager
from BoundingBoxManager import BoundingBoxManager
from BoundingBoxDisplay import BoundingBoxDisplay

from random import randint, uniform

class BoundingBoxFineTuner :

    """ Precisely finetune bounding boxes """

    def __init__(self, window, bboxDisplay, imageDisplay=None, displayWidth=400, displayHeight=400, bboxIncrement=0.02) :
        """
        <window> : The Tkinter window where the map should be displayed
        <displayWidth> : Width of the display
        <displayHeight> : Height of the display
        """
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()

        self.imageDisplay = imageDisplay
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        self.bboxDisplay = bboxDisplay

        self.bboxIncrement = bboxIncrement

        # Blanck canvas
        self.canvas = Canvas(self.frame, width=self.displayWidth, height=self.displayHeight)
        self.canvas.create_rectangle(1, 1, self.displayWidth, self.displayHeight)
        self.canvas.focus()

        self.canvas.bind("<Right>", self.lengthenBboxHorizontally)
        self.canvas.bind("<Left>", self.shortenBboxHorizontally)
        self.canvas.bind("<Up>", self.lengthenBboxVertically)
        self.canvas.bind("<Down>", self.shortenBboxVertically)

        self.canvas.bind("<q>", self.moveBboxLeft)
        self.canvas.bind("<Q>", self.moveBboxLeft)
        self.canvas.bind("<d>", self.moveBboxRight)
        self.canvas.bind("<D>", self.moveBboxRight)
        self.canvas.bind("<z>", self.moveBboxUp)
        self.canvas.bind("<Z>", self.moveBboxUp)
        self.canvas.bind("<s>", self.moveBboxDown)
        self.canvas.bind("<S>", self.moveBboxDown)

        self.canvas.focus_set() # How does this interract with other stuff ?

        self.bbox = None

        self.canvas.pack(pady=10)

        self.loadedImage_backup = None
        self.loadedImage_backupPath = ""


    def getBbox(self) :
        i_bbox = self.bboxDisplay.i_selectedBbox
        if (i_bbox is None) :
            return None
        imagePath = self.bboxDisplay.currentlyShownImagePath
        if (imagePath is None) :
            return None
        try :
            return self.bboxDisplay.bboxManager.boundingBoxes[imagePath][i_bbox]
        except :
            return None
    def bboxIsValid(self) :
        return self.getBbox() is not None
    def getBboxLeft(self) : return self.getBbox()["left_percentage"]
    def getBboxRight(self) : return self.getBbox()["right_percentage"]
    def getBboxTop(self) : return self.getBbox()["top_percentage"]
    def getBboxBottom(self) : return self.getBbox()["bottom_percentage"]
    def setBboxLeft(self, val) : self.getBbox()["left_percentage"] = val
    def setBboxRight(self, val) : self.getBbox()["right_percentage"] = val
    def setBboxTop(self, val) : self.getBbox()["top_percentage"] = val
    def setBboxBottom(self, val) : self.getBbox()["bottom_percentage"] = val



    def updateImage(self) :
        imagePath = self.bboxDisplay.currentlyShownImagePath
        if (imagePath is None) :
            return
        try :
            if (self.loadedImage_backupPath != imagePath) :
                print("load new image")
                self.loadedImage_backup = cv2.imread(imagePath)
                self.loadedImage_backupPath = imagePath
            self.image = self.loadedImage_backup
        except :
            print(f"[Warning] : Cannot read image '{imagePath}'")
            return

        if not(self.bboxIsValid()) :
            return

        imageHeight, imageWidth, n_channels = self.image.shape

        horizontalRange = self.getBboxRight() - self.getBboxLeft()
        verticalRange = self.getBboxBottom() - self.getBboxTop()

        imageLeftPercentage = max(0, self.getBboxLeft() - 0.1 * horizontalRange)
        imageRightPercentage = min(1, self.getBboxRight() + 0.1 * horizontalRange)
        imageBottomPercentage = min(1, self.getBboxBottom() + 0.1 * verticalRange)
        imageTopPercentage = max(0, self.getBboxTop() - 0.1 * verticalRange)

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

        bboxLeftPixel_onScreen = int(1 + (self.displayWidth - 2) * updateProp(self.getBboxLeft(), imageLeftPercentage, imageRightPercentage))
        bboxRightPixel_onScreen = int((self.displayWidth - 2) * updateProp(self.getBboxRight(), imageLeftPercentage, imageRightPercentage))
        bboxBottomPixel_onScreen = int((self.displayHeight - 2) * updateProp(self.getBboxBottom(), imageTopPercentage, imageBottomPercentage))
        bboxTopPixel_onScreen = int(1 + (self.displayHeight - 2) * updateProp(self.getBboxTop(), imageTopPercentage, imageBottomPercentage))

        self.canvas.create_rectangle(bboxLeftPixel_onScreen, bboxTopPixel_onScreen, bboxRightPixel_onScreen, bboxBottomPixel_onScreen, width=3)
        color = None
        bbox = self.getBbox()
        if (bbox is not None) :
            category = bbox["category"]
            if (category is not None) :
                color = "#%02x%02x%02x" % tuple(category['color_rgb'])
        self.canvas.create_rectangle(bboxLeftPixel_onScreen, bboxTopPixel_onScreen, bboxRightPixel_onScreen, bboxBottomPixel_onScreen, outline=color)

    def shortenBboxHorizontally(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxHorizontalRange = self.getBboxRight() - self.getBboxLeft()
        self.setBboxRight(max(0, self.getBboxRight() - self.bboxIncrement * bboxHorizontalRange))
        self.setBboxLeft(min(1, self.getBboxLeft() + self.bboxIncrement * bboxHorizontalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()


    def lengthenBboxHorizontally(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxHorizontalRange = self.getBboxRight() - self.getBboxLeft()
        self.setBboxRight(min(1, self.getBboxRight() + self.bboxIncrement * bboxHorizontalRange))
        self.setBboxLeft(max(0, self.getBboxLeft() - self.bboxIncrement * bboxHorizontalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()

    def shortenBboxVertically(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxVerticalRange = self.getBboxBottom() - self.getBboxTop()
        self.setBboxTop(min(1, self.getBboxTop() + self.bboxIncrement * bboxVerticalRange))
        self.setBboxBottom(max(0, self.getBboxBottom() - self.bboxIncrement * bboxVerticalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()

    def lengthenBboxVertically(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxVerticalRange = self.getBboxBottom() - self.getBboxTop()
        self.setBboxTop(max(0, self.getBboxTop() - self.bboxIncrement * bboxVerticalRange))
        self.setBboxBottom(min(1, self.getBboxBottom() + self.bboxIncrement * bboxVerticalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()

    def moveBboxUp(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxVerticalRange = self.getBboxBottom() - self.getBboxTop()
        self.setBboxTop(max(0, self.getBboxTop() - self.bboxIncrement * bboxVerticalRange))
        self.setBboxBottom(max(0, self.getBboxBottom() - self.bboxIncrement * bboxVerticalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()

    def moveBboxDown(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxVerticalRange = self.getBboxBottom() - self.getBboxTop()
        self.setBboxTop(min(1, self.getBboxTop() + self.bboxIncrement * bboxVerticalRange))
        self.setBboxBottom(min(1, self.getBboxBottom() + self.bboxIncrement * bboxVerticalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()

    def moveBboxLeft(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxHorizontalRange = self.getBboxRight() - self.getBboxLeft()
        self.setBboxRight(max(0, self.getBboxRight() - self.bboxIncrement * bboxHorizontalRange))
        self.setBboxLeft(max(0, self.getBboxLeft() - self.bboxIncrement * bboxHorizontalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()

    def moveBboxRight(self, event=None) :
        if not(self.bboxIsValid()) :
            return
        bboxHorizontalRange = self.getBboxRight() - self.getBboxLeft()
        self.setBboxRight(min(1, self.getBboxRight() + self.bboxIncrement * bboxHorizontalRange))
        self.setBboxLeft(min(1, self.getBboxLeft() + self.bboxIncrement * bboxHorizontalRange))
        self.updateImage()
        self.bboxDisplay.updateTable(self.bboxDisplay.currentlyShownImagePath)
        if (self.imageDisplay is not None) : self.imageDisplay.updateImage()


if __name__ == "__main__" :

    window = tk.Tk()
    window.title("BBoxFineTuner")
    window.geometry('1300x800')

    categoryManager = testCategoryManager()
    bboxManager = BoundingBoxManager()
    for _ in range(100) :
        category = categoryManager.categories[randint(0, len(categoryManager.categories)) - 1]
        bboxManager.addBoundingBox("/home/nicolas/labellingTool/data/aaJPGlabel.jpeg", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=category)
    for _ in range(100) :
        bboxManager.addBoundingBox("/home/nicolas/labellingTool/data/aaJPGlabel.jpeg", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=categoryManager.categories[0])

    bboxDisplay = BoundingBoxDisplay(window, bboxManager)

    bboxTuner = BoundingBoxFineTuner(window, bboxDisplay)
    bboxTuner.frame.place(x=40, y=50)


    bboxTuner.updateImage()

    exitButton = tk.Button(window, text='close window', width=10, command=window.destroy)
    exitButton.pack()

    window.mainloop()
