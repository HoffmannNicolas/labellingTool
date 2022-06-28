
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

from BoundingBoxManager import BoundingBoxManager


class ImageDisplay :


    """ Area where the image is displayed and boundingBoxes can be drawn with the mouse """


    def __init__(self, window, boundingBoxManager, displayWidth=700, displayHeight=700) :
        """
        <window> : The Tkinter window where the map should be displayed
        <displayWidth> : Width of the display
        <displayHeight> : Height of the display
        """
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.boundingBoxManager = boundingBoxManager
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight

        self.topHeightMargin = 60
        self.bottomHeightMargin = 25

        self.imageWidth = displayWidth
        self.imageHeight = displayHeight - self.topHeightMargin - self.bottomHeightMargin

        # Blanck canvas
        self.canvas = Canvas(self.frame, width=self.displayWidth, height=self.displayHeight)
        self.canvas.bind("<ButtonPress-1>", self.leftClickPress)
        self.canvas.bind("<ButtonRelease-1>", self.leftClickRelease)
        self.canvas.bind("<B1-Motion>", self.drag)

        # Folder selection
        self.loadButton = tk.Button(self.canvas, text="Load Folder", width=8, command=self.load, bg="white")
        self.loadButtonWindow = self.canvas.create_window(3, 0, window=self.loadButton, anchor="nw")
        self.folderLabel = tk.Label(self.frame, text=":")
        self.canvas.create_window(95, 5, window=self.folderLabel, anchor="nw")
        self.folderPath = tk.StringVar(self.frame, value="/home/nicolas/labellingTool/data") # "/path/to/image/folder/"
        self.folderPathWindow = tk.Entry(self.window, width=73, textvariable=self.folderPath)
        self.folderPathWindow.bind('<Return>', self.updateFolderPath) # Bind update to return presses
        self.canvas.create_window(105, 5, window=self.folderPathWindow, anchor="nw")
        self.imagePaths = []

        # Image selection
        self.imageLabel = tk.Label(self.frame, text="Image :")
        self.canvas.create_window(3, self.topHeightMargin / 2, window=self.imageLabel, anchor="nw")
        self.imageIndex = tk.IntVar(self.frame, value=0)
        self.imageIndexWindow = tk.Entry(self.window, width=7, textvariable=self.imageIndex, justify="center")
        self.imageIndexWindow.bind('<Return>', self.updateImageIndex) # Bind update to return presses
        self.canvas.create_window(58, self.topHeightMargin / 2, window=self.imageIndexWindow, anchor="nw")
        self.n_images = 0
        self.over = tk.Label(self.frame, text=f"/ {self.n_images}")
        self.canvas.create_window(120, self.topHeightMargin / 2, window=self.over, anchor="nw")
        self.imagePath = tk.StringVar(self.frame, value="/path/to/image/img.png")
        self.imagePathWindow = tk.Entry(self.window, width=65, textvariable=self.imagePath)
        self.imagePathWindow.bind('<Return>', self.updateImagePath) # Bind update to return presses
        self.canvas.create_window(169, self.topHeightMargin / 2, window=self.imagePathWindow, anchor="nw")

        # Checkboxes
        self.deform = tk.IntVar()
        self.deformCheckbox = tk.Checkbutton(self.frame, text="Deform Image", variable=self.deform, onvalue=1, offvalue=0, command=self.updateImage)
        self.canvas.create_window(self.displayWidth / 2, self.displayHeight - self.bottomHeightMargin / 2, window=self.deformCheckbox)

        # Image
        self.imageArea = self.canvas.create_rectangle(0, self.topHeightMargin, self.imageWidth, self.displayHeight - self.bottomHeightMargin, outline="black",fill="black")
        self.updateImage()

        self.canvas.pack(pady=10)

        self.bboxWannabe_1 = None # Draw bbox being created
        self.bboxWannabe_2 = None

        self.loadedImage = None

        self.imageName = None

        self.boundingBoxesReferences = []


    def updateImageIndex(self, event) :
        if (self.n_images <= 0 and self.imageIndex.get() < 0) :
            self.imageIndex.set(0)
        if (self.n_images > 0 and self.imageIndex.get() < 0) :
            self.imageIndex.set(1)
        if (self.imageIndex.get() > self.n_images) :
            self.imageIndex.set(self.n_images)
        self.updateImage()

    def updateImagePath(self, event) :
        newImagePath = self.imagePath.get()
        if (newImagePath in self.imagePaths) :
            i = self.imagePaths.index(newImagePath)
        else :
            i = self.imageIndex.get() - 1
        self.imageIndex.set(i + 1)
        self.updateImage()

    def updateImage(self) :
        # Load image
        if (self.n_images <= 0) :
            print("No image to display")
            self.image = None
            return
        try :
            imagePath = self.imagePaths[self.imageIndex.get() - 1]
            self.loadedImage = cv2.imread(imagePath)
        except :
            print(f"[Warning] : Cannot read image '{imagePath}'")

        # Update display
        self.imagePath.set(imagePath)
        self.imageName = imagePath.split("/")[-1].split(".")[0]

        # Resize image
        if (self.deform.get() == 1) :
            newWidth = self.imageWidth
            newHeight = self.imageHeight
        else :
            height, width, n_channel = self.loadedImage.shape # Height and width inverted here
            w_ratio = self.imageWidth / width
            h_ratio = self.imageHeight / height
            ratio = min(w_ratio, h_ratio)
            newWidth = int(width * ratio)
            newHeight = int(height * ratio)
        self.loadedImage = cv2.resize(self.loadedImage, [newWidth, newHeight], interpolation = cv2.INTER_AREA)

        # Display image at proper position
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.loadedImage))
        x_position = int((self.imageWidth - newWidth) / 2)
        y_position = self.topHeightMargin + int((self.imageHeight - newHeight) / 2)
        self.view = self.canvas.create_image(x_position, y_position, anchor="nw", image=self.image)

        self.drawBoundingBoxes()

    def drawBoundingBoxes(self) :

        for boundingBoxReference in self.boundingBoxesReferences :
            self.canvas.delete(boundingBoxReference)

        if (self.imageName in list(self.boundingBoxManager.boundingBoxes.keys())) :
            for boundingBox in self.boundingBoxManager.boundingBoxes[self.imageName] :
                left_pixel, top_pixel = self.computeImagePixels(boundingBox.left_percentage, boundingBox.top_percentage)
                right_pixel, bottom_pixel = self.computeImagePixels(boundingBox.right_percentage, boundingBox.bottom_percentage)
                bboxRef = self.canvas.create_rectangle(
                    left_pixel,
                    top_pixel,
                    right_pixel,
                    bottom_pixel,
                    width=1,
                    outline="black"
                )
                self.boundingBoxesReferences.append(bboxRef)


    def updateFolderPath(self, event) :
        self.load()

    def load(self) :
        """ Load a database from its path """
        extensions = ["png", "jpg", "jpeg"]
        self.imagePaths = []
        for extension in extensions :
            self.imagePaths.extend(list(glob.glob(f"{self.folderPath.get()}/*.{extension}")))
        self.imagePaths.sort()
        self.n_images = len(self.imagePaths)
        self.over.configure(text=f"/ {self.n_images}")
        if (self.n_images > 0) :
            self.imageIndex.set(1)
        else :
            self.imageIndex.set(0)
        self.updateImage()


    def computeImagePercentages(self, x_pixel, y_pixel) :
        if (self.loadedImage is None) :
            return 0, 0
        img_height, img_width, n_channel = self.loadedImage.shape
        img_left = int((self.imageWidth - img_width) / 2)
        img_top = self.topHeightMargin + int((self.imageHeight - img_height) / 2)
        x_percentage = (x_pixel - img_left) / img_width
        y_percentage = (y_pixel - img_top) / img_height
        return x_percentage, y_percentage

    def computeImagePixels(self, x_percentage, y_percentage) :
        if (self.loadedImage is None) :
            return 0, 0
        img_height, img_width, n_channel = self.loadedImage.shape
        img_left = int((self.imageWidth - img_width) / 2)
        img_top = self.topHeightMargin + int((self.imageHeight - img_height) / 2)
        x_pixel = x_percentage * img_width + img_left
        y_pixel = y_percentage * img_height + img_top
        return x_pixel, y_pixel

    def getBoundingBoxCoordinate_percentage(self) :
        top_pixel = min(self.y_click, self.y_drag)
        right_pixel = max(self.x_click, self.x_drag)
        bottom_pixel = max(self.y_click, self.y_drag)
        left_pixel = min(self.x_click, self.x_drag)
        left_percentage, top_percentage = self.computeImagePercentages(left_pixel, top_pixel)
        right_percentage, bottom_percentage = self.computeImagePercentages(right_pixel, bottom_pixel)

        left_percentage = max(0, left_percentage)
        left_percentage = min(1, left_percentage)
        top_percentage = max(0, top_percentage)
        top_percentage = min(1, top_percentage)
        right_percentage = max(0, right_percentage)
        right_percentage = min(1, right_percentage)
        bottom_percentage = max(0, bottom_percentage)
        bottom_percentage = min(1, bottom_percentage)

        return left_percentage, top_percentage, right_percentage, bottom_percentage

    def getBoundingBoxCoordinate_pixel(self) :
        left_percentage, top_percentage, right_percentage, bottom_percentage = self.getBoundingBoxCoordinate_percentage()
        left_pixel, top_pixel = self.computeImagePixels(left_percentage, top_percentage)
        right_pixel, bottom_pixel = self.computeImagePixels(right_percentage, bottom_percentage)
        return left_pixel, top_pixel, right_pixel, bottom_pixel

    def leftClickPress(self, event) :
        self.x_click = event.x
        self.y_click = event.y

    def drag(self, event):
        self.x_drag = event.x
        self.y_drag = event.y

        left_pixel, top_pixel, right_pixel, bottom_pixel = self.getBoundingBoxCoordinate_pixel()
        if (self.bboxWannabe_1 is not None) :
            self.canvas.delete(self.bboxWannabe_1)
            self.canvas.delete(self.bboxWannabe_2)
        self.bboxWannabe_1 = self.canvas.create_rectangle(left_pixel, top_pixel, right_pixel, bottom_pixel, width=3, outline="black")
        self.bboxWannabe_2 = self.canvas.create_rectangle(left_pixel, top_pixel, right_pixel, bottom_pixel, width=1, outline="white")


    def leftClickRelease(self, event) :
        self.canvas.delete(self.bboxWannabe_1)
        self.canvas.delete(self.bboxWannabe_2)

        left_percentage, top_percentage, right_percentage, bottom_percentage = self.getBoundingBoxCoordinate_percentage()
        self.boundingBoxManager.addBoundingBox(self.imageName, left_percentage, top_percentage, right_percentage, bottom_percentage)

        self.drawBoundingBoxes()


if __name__ == "__main__" :

    window = tk.Tk()
    window.title("Detector")
    window.geometry('1300x800')

    bboxManager = BoundingBoxManager()
    imageDisplay = ImageDisplay(window, bboxManager)
    imageDisplay.frame.place(x=400, y=50)

    exitButton = tk.Button(window, text='close window', width=10, command=window.destroy)
    exitButton.pack()

    window.mainloop()