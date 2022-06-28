
import tkinter as tk

from ImageDisplay import ImageDisplay
from CategoryManager import CategoryManager, CategoryDisplay
from BoundingBoxManager import BoundingBoxManager, BoundingBoxDisplay

from Category import Category

from random import randint, uniform


window = tk.Tk()
window.title("Detector")
window.geometry('1600x800')

categoryManager = CategoryManager()
categoryManager.addCategory(Category(name="Cat", color_rgb=[200, 200, 0]))
categoryManager.addCategory(Category(name="Human", color_rgb=[230, 120, 0]))
categoryManager.addCategory(Category(name="Robot", color_rgb=[100, 100, 100]))
categoryManager.addCategory(Category(name="Overlord", color_rgb=[60, 60, 100]))
categoryManager.addCategory(Category(name="Snowboard", color_rgb=[230, 230, 255]))
categoryManager.addCategory(Category(name="Sun", color_rgb=[255, 255, 180]))
categoryManager.addCategory(Category(name="Lava", color_rgb=[200, 60, 0]))
categoryManager.addCategory(Category(name="Water", color_rgb=[110, 110, 200]))
categoryManager.addCategory(Category(name="Tree", color_rgb=[20, 80, 20]))
categoryManager.addCategory(Category(name="Dispear", color_rgb=[666, 666, 666]))
categoryManager.addCategory(Category(name="Git", color_rgb=[0, 0, 0]))
categoryManager.addCategory(Category(name="Catpuccino", color_rgb=[255, 220, 20]))

categoryDisplay = CategoryDisplay(window, categoryManager)


bboxManager = BoundingBoxManager()
for _ in range(100) :
    category = categoryManager.categories[randint(0, len(categoryManager.categories)) - 1]
    bboxManager.addBoundingBox("imagePath", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=category)
bboxDisplay = BoundingBoxDisplay(window, bboxManager)
bboxDisplay.updateTable("imagePath")

imageDisplay = ImageDisplay(window, bboxManager)

exitButton = tk.Button(window, text='close window', width=10, command=window.destroy)
exitButton.pack()
exitButton.place(x=800, y=750)


categoryDisplay.frame.place(x=3, y=3)
imageDisplay.frame.place(x=300, y=3)
bboxDisplay.frame.place(x=1050, y=3)


window.mainloop()
