
from BoundingBox import BoundingBox

from random import randint, uniform

from tkinter import *
from  tkinter import ttk

from random import randint
from CategoryManager import CategoryManager

from Category import Category


class BoundingBoxManager :

    """ Manages all the bounding boxes, shared between all elements of the interface """

    def __init__(self) :
        self.boundingBoxes = {}


    def addBoundingBox(self, imagePath, top, right, bottom, left, category=None) :
        if (imagePath not in list(self.boundingBoxes.keys())) :
            self.boundingBoxes[imagePath] = []
        self.boundingBoxes[imagePath].append(BoundingBox(top, right, bottom, left, category))


class BoundingBoxDisplay :

    def __init__(self, window, bboxManager) :

        self.window = window
        self.bboxManager = bboxManager

        self.frame = Frame(window)
        self.frame.pack()

        # Scrollbar
        self.scroll = Scrollbar(self.frame)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(self.frame, yscrollcommand=self.scroll.set)
        self.table.pack()

        self.scroll.config(command=self.table.yview)
        self.scroll.config(command=self.table.xview)

        # Columns
        self.table['columns'] = ("Class", "Left %", "Top %", "Right %", "Bottom %", "Index")
        self.table.column("#0", width=0, stretch=NO)
        self.table.column("Class", anchor=CENTER, width=100)
        self.table.column("Left %", anchor=CENTER, width=80)
        self.table.column("Top %", anchor=CENTER, width=80)
        self.table.column("Right %", anchor=CENTER, width=80)
        self.table.column("Bottom %", anchor=CENTER, width=80)
        self.table.column("Index", anchor=CENTER, width=80)

        # Headings
        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("Class", text="Class", anchor=CENTER)
        self.table.heading("Left %", text="Left %", anchor=CENTER)
        self.table.heading("Top %", text="Top %", anchor=CENTER)
        self.table.heading("Right %", text="Right %", anchor=CENTER)
        self.table.heading("Bottom %", text="Bottom %", anchor=CENTER)
        self.table.heading("Index", text="Index", anchor=CENTER)

        self.table.pack()


    def updateTable(self, imagePath) :

        for row in self.table.get_children():
            self.table.delete(row)

        for i, bbox in enumerate(self.bboxManager.boundingBoxes[imagePath]) :
            name = f"{bbox.category.name}"
            left = f"{round(bbox.left_percentage, 3)}"
            top = f"{round(bbox.top_percentage, 3)}"
            right = f"{round(bbox.right_percentage, 3)}"
            bottom = f"{round(bbox.bottom_percentage, 3)}"
            tag = (f"category_{bbox.category.name}")
            self.table.insert(parent='', index='end', text='', values=(name, left, top, right, bottom, i), tags=tag)
            self.table.tag_configure(f"category_{bbox.category.name}", background ="#%02x%02x%02x" % tuple(bbox.category.color_rgb))




if __name__ == "__main__" :

    window  = Tk()
    window.geometry('500x500')
    window['bg'] = "black"

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

    bboxManager = BoundingBoxManager()
    for _ in range(100) :
        category = categoryManager.categories[randint(0, len(categoryManager.categories)) - 1]
        bboxManager.addBoundingBox("imagePath", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=category)

    for _ in range(100) :
        bboxManager.addBoundingBox("imagePath2", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=categoryManager.categories[0])

    bboxDisplay = BoundingBoxDisplay(window, bboxManager)
    bboxDisplay.updateTable("imagePath")
    bboxDisplay.updateTable("imagePath2")
    bboxDisplay.updateTable("imagePath")

    window.mainloop()
