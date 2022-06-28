from tkinter import *
from  tkinter import ttk

from random import randint

from Category import Category


class CategoryManager :

    """ Deal with categories shared between all objects of the interface """

    def __init__(self, categories=[]) :
        self.categories = categories

    def addCategory(self, category) :
        self.categories.append(category)


class CategoryDisplay :

    def __init__(self, window, categoryManager) :

        self.window = window
        self.categoryManager = categoryManager

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
        self.table['columns'] = ('Name', 'Color', 'Index')
        self.table.column("#0", width=0, stretch=NO)
        self.table.column("Name", anchor=CENTER, width=100)
        self.table.column("Color", anchor=CENTER, width=120)
        self.table.column("Index", anchor=CENTER, width=45)

        # Headings
        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("Name", text="Name", anchor=CENTER)
        self.table.heading("Color", text="Color", anchor=CENTER)
        self.table.heading("Index", text="Index", anchor=CENTER)

        # Data
        for i, category in enumerate(categoryManager.categories) :
            self.table.insert(parent='', index='end', text='', values=(f"{category.name}", f"{category.color_rgb}", f"{i}"), tags=(f"category_{i}"))
            self.table.tag_configure(f"category_{i}", background ="#%02x%02x%02x" % tuple(category.color_rgb))

        self.table.pack()



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

    categoryDisplay = CategoryDisplay(window, categoryManager)

    window.mainloop()
