
import tkinter as tk

from ImageDisplay import ImageDisplay

from CategoryManager import CategoryManager
from CategoryDisplay import CategoryDisplay

from BoundingBoxManager import BoundingBoxManager
from BoundingBoxDisplay import BoundingBoxDisplay


window = tk.Tk()
window.title("Detector")
window.geometry('1600x800')

categoryManager = CategoryManager()
categoryDisplay = CategoryDisplay(window, categoryManager)

bboxManager = BoundingBoxManager()
bboxDisplay = BoundingBoxDisplay(window, bboxManager)
# bboxDisplay.updateTable("imagePath")

imageDisplay = ImageDisplay(window, bboxManager, bboxDisplay, categoryManager, categoryDisplay)

exitButton = tk.Button(window, text='close window', width=10, command=window.destroy)
exitButton.pack()
exitButton.place(x=800, y=750)


categoryDisplay.frame.place(x=3, y=3)
imageDisplay.frame.place(x=300, y=3)
bboxDisplay.frame.place(x=1050, y=3)


window.mainloop()
