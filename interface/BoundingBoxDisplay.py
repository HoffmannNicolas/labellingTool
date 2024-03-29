

from BoundingBoxManager import BoundingBoxManager

from random import randint, uniform

from tkinter import *
from  tkinter import ttk

from random import randint
from CategoryManager import CategoryManager, testCategoryManager

class BoundingBoxDisplay :

    """ The table displaying the content of a BoundingBoxManager, as a tkinter frame """

    def __init__(self, window, bboxManager, bboxTuner=None) :

        self.window = window
        self.bboxManager = bboxManager
        self.bboxTuner = bboxTuner

        self.frame = Frame(window)
        self.frame.pack()

        # Scrollbar
        self.scroll = Scrollbar(self.frame)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(self.frame, yscrollcommand=self.scroll.set)
        self.table.pack()
        self.table.bind('<<TreeviewSelect>>', self.on_select)
        self.i_selectedBbox = None

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

        self.currentlyShownImagePath = None


    def updateTable(self, imagePath=None) :

        if (imagePath is None) :
            imagePath = self.currentlyShownImagePath

        for row in self.table.get_children():
            self.table.delete(row)

        if not(imagePath in list(self.bboxManager.boundingBoxes.keys())) :
            # No bbox for this image, yet
            return


        for i, bbox in enumerate(self.bboxManager.boundingBoxes[imagePath]) :
            if (bbox["category"] is None) :
                categoryName = "None"
                categoryColor_rgb = [128, 128, 128]
            else :
                categoryName = f"{bbox['category']['name']}"
                categoryColor_rgb = bbox['category']['color_rgb']
            left = f"{round(bbox['left_percentage'], 3)}"
            top = f"{round(bbox['top_percentage'], 3)}"
            right = f"{round(bbox['right_percentage'], 3)}"
            bottom = f"{round(bbox['bottom_percentage'], 3)}"
            tag = (f"category_{categoryName}")
            self.table.insert(parent='', index='end', text='', values=(categoryName, left, top, right, bottom, i), tags=tag)
            self.table.tag_configure(f"category_{categoryName}", background ="#%02x%02x%02x" % tuple(categoryColor_rgb))

        imageBboxes = self.bboxManager.boundingBoxes[imagePath]
        if (self.i_selectedBbox is None) :
            if (len(imageBboxes) > 0) :
                self.i_selectedBbox = 0
            else :
                self.i_selectedBbox = None
        self.currentlyShownImagePath = imagePath


    def on_select(self, event=None) :
        focus = self.table.focus()
        item = self.table.item(focus, "values")
        self.i_selectedBbox = int(item[-1])
        if (self.bboxTuner is not None) :
            self.bboxTuner.updateImage()

    def moveToNextBbox(self, event=None) :
        print(self.i_selectedBbox)
        if (self.currentlyShownImagePath is None) :
            self.i_selectedBbox = None
        else :
            imageBboxes = self.bboxManager.boundingBoxes[self.currentlyShownImagePath]
            n_bboxes = len(imageBboxes)
            print(n_bboxes)
            if (n_bboxes <= 0) :
                self.i_selectedBbox = None
            else :
                self.i_selectedBbox = (self.i_selectedBbox + 1) % n_bboxes
                print(self.i_selectedBbox)
        self.updateTable()
        print(self.i_selectedBbox)


if __name__ == "__main__" :

    window  = Tk()
    window.geometry('1000x800')
    window['bg'] = "black"

    categoryManager = testCategoryManager()
    bboxManager = BoundingBoxManager()
    for _ in range(100) :
        category = categoryManager.categories[randint(0, len(categoryManager.categories)) - 1]
        bboxManager.addBoundingBox("imagePath", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=category)
    for _ in range(100) :
        bboxManager.addBoundingBox("imagePath2", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=categoryManager.categories[0])

    bboxDisplay = BoundingBoxDisplay(window, bboxManager)
    bboxDisplay.frame.place(x=50, y=300)
    bboxDisplay.updateTable("imagePath")
    bboxDisplay.updateTable("imagePath2")
    bboxDisplay.updateTable("imagePath")

    window.mainloop()
