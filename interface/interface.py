
import tkinter as tk
from tkinter import *

from ImageDisplay import ImageDisplay

from CategoryManager import CategoryManager
from CategoryDisplay import CategoryDisplay

from BoundingBoxManager import BoundingBoxManager
from BoundingBoxDisplay import BoundingBoxDisplay
from BoundingBoxFineTuner import BoundingBoxFineTuner


class DetectionLabellingInterface :

    """ Labelling interface dedicated to detection, allows to draw labeled bounding boxes around objects in an image """

    def __init__(self, window, width=1300, height=800, margin=5) :

        self.window = window
        self.width = width
        self.height = height
        self.margin = margin
        self.frame = Frame(window)
        self.frame.pack()
        self.canvas = Canvas(self.frame, width=self.width, height=self.height)
        self.canvas.create_rectangle(1, 1, self.width-2, self.height-2)
        self.canvas.pack()

        self.categoryManager = CategoryManager()
        self.categoryDisplay = CategoryDisplay(
            self.frame,
            self.categoryManager
        )

        self.bboxManager = BoundingBoxManager()
        self.bboxDisplay = BoundingBoxDisplay(
            self.frame,
            self.bboxManager
        )
        self.bboxTuner = BoundingBoxFineTuner(
            self.frame,
            self.bboxDisplay,
            displayWidth=0.3*self.width-2*self.margin,
            displayHeight=0.4*self.height-2*self.margin
        )
        self.bboxDisplay.bboxTuner = self.bboxTuner
        # bboxDisplay.updateTable("imagePath")

        self.imageDisplay = ImageDisplay(
            self.frame,
            self.bboxManager,
            self.bboxDisplay,
            self.categoryManager,
            self.categoryDisplay,
            bboxTuner=self.bboxTuner,
            displayWidth=0.5*self.width-2*self.margin,
            displayHeight=self.height-2*self.margin
        )
        self.bboxTuner.imageDisplay = self.imageDisplay

        self.categoryDisplay.frame.place(x=self.margin, y=self.margin)
        self.imageDisplay.frame.place(x=int(0.2*width+self.margin), y=self.margin)
        self.bboxDisplay.frame.place(x=int(0.8*width+self.margin), y=self.margin)
        self.bboxTuner.frame.place(x=int(0.7*width+self.margin), y=int(0.6*height+self.margin))

        self.saveBoxesButton = tk.Button(self.frame, text="S[a]ve Boxes", width=10, command=self.saveBoxes)
        self.saveBoxesButton.pack()
        self.saveBoxesButton.place(x=int(0.05*self.width), y=int(0.9*self.height), anchor="center")

        self.undoButton = tk.Button(self.frame, text="[U]ndo", width=10, command=self.undo)
        self.undoButton.pack()
        self.undoButton.place(x=0.15* self.width, y=0.9*self.height, anchor="center")

        self.exitButton = tk.Button(self.frame, text='close window', width=10, command=window.destroy)
        self.exitButton.pack()
        self.exitButton.place(x=0.05* self.width, y=0.95*self.height, anchor="center")

        self.previousImage_x = int(0.1*self.width)
        self.previousImage_h = int(0.5*self.height)
        self.previousImageButton = tk.Button(self.frame, text="Previous Image", width=11, command=self.previousImage)
        self.previousImageButton.pack()
        self.previousImageButton.place(x=self.previousImage_x, y=self.previousImage_h, anchor="center")
        self.drawArrow([self.previousImage_x + 50, self.previousImage_h], [self.previousImage_x - 50, self.previousImage_h])

        self.nextImage_x = int(0.9*self.width)
        self.nextImage_h = int(0.5*self.height)
        self.nextImageButton = tk.Button(self.frame, text="Next Image\n[Return]", width=11, command=self.nextImage)
        self.nextImageButton.pack()
        self.nextImageButton.place(x=self.nextImage_x, y=self.nextImage_h, anchor="center")
        self.drawArrow([self.nextImage_x - 50, self.nextImage_h], [self.nextImage_x + 50, self.nextImage_h])

        self.window.bind("<a>", self.saveBoxes)
        self.window.bind("<u>", self.undo)
        self.window.bind("<Return>", self.nextImage)
        self.window.bind("<space>", self.nextBbox)

        self.window.bind("<Right>", self.bboxTuner.lengthenBboxHorizontally)
        self.window.bind("<Left>", self.bboxTuner.shortenBboxHorizontally)
        self.window.bind("<Up>", self.bboxTuner.lengthenBboxVertically)
        self.window.bind("<Down>", self.bboxTuner.shortenBboxVertically)

        self.window.bind("<q>", self.bboxTuner.moveBboxLeft)
        self.window.bind("<Q>", self.bboxTuner.moveBboxLeft)
        self.window.bind("<d>", self.bboxTuner.moveBboxRight)
        self.window.bind("<D>", self.bboxTuner.moveBboxRight)
        self.window.bind("<z>", self.bboxTuner.moveBboxUp)
        self.window.bind("<Z>", self.bboxTuner.moveBboxUp)
        self.window.bind("<s>", self.bboxTuner.moveBboxDown)
        self.window.bind("<S>", self.bboxTuner.moveBboxDown)

        """
        # Checkboxes
        self.deform = tk.IntVar()
        self.deformCheckbox = tk.Checkbutton(self.frame, text="Deform Image", variable=self.deform, onvalue=1, offvalue=0, command=self.updateImage)
        self.canvas.create_window(self.displayWidth / 2, self.displayHeight - self.bottomHeightMargin / 2, window=self.deformCheckbox)

        """

    def drawArrow(self, base, tip) :
        bx = base[0]
        by = base[1]
        direction = [tip[0] - base[0], tip[1] - base[1]]
        dx = direction[0]
        dy = direction[1]
        l = [dx / 3, dy / 3] # "Unit" vector from base toward tip
        lx = l[0]
        ly = l[1]
        w = [-l[1], l[0]] # "Unit" vector sideways, to the left
        wx = w[0]
        wy = w[1]
        A = [bx + wx - lx, by + wy - ly]
        B = [bx + wx + 3*lx, by + wy + 3*ly]
        C = [bx + 3*lx + 2*wx, by + 3*ly + 2*wy]
        D = [bx + 5*lx, by + 5*ly]
        E = [bx + 3*lx -2*wx, by + 3*ly -2*wy]
        F = [bx + 3*lx - wx, by + 3*ly - wy]
        G = [bx - lx - wx, by - ly - wy]
        for p1, p2 in [[A, B], [B, C], [C, D], [D, E], [E, F], [F, G], [G, A]] :
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1])


    def nextBbox(self, event=None) :
        self.bboxDisplay.moveToNextBbox()
        self.bboxTuner.updateImage()
        print("nexwt bbox")

    def previousImage(self, event=None) :
        return self.changeImageIndex(change=-1)

    def nextImage(self, event=None) :
        return self.changeImageIndex(change=1)

    def changeImageIndex(self, change=1) :
        newIndex = self.imageDisplay.imageIndex.get() + change
        self.imageDisplay.imageIndex.set(newIndex)
        self.imageDisplay.updateImageIndex()
        self.bboxDisplay.updateTable(self.imageDisplay.imagePath.get())
        self.bboxTuner.updateImage()

    def saveBoxes(self, event=None) :
        self.bboxManager.saveToFolder(self.imageDisplay.folderPath.get())
        print("Bounding Boxes saved")

    def undo(self, event=None) :
        self.bboxManager.deleteLastBbox(self.imageDisplay.imagePath.get())
        self.bboxDisplay.updateTable(self.imageDisplay.imagePath.get())
        self.imageDisplay.drawBoundingBoxes()
        print("Undone")


if __name__ == "__main__" :

    window = tk.Tk()
    window.title("Detector")
    w = 1760
    h = 830
    window.geometry(f"{w}x{h}")

    detectionLabellingInterface = DetectionLabellingInterface(window, width=w, height=h)

    window.mainloop()
