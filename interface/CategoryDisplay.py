
from tkinter import *
from  tkinter import ttk

from random import randint

from CategoryManager import CategoryManager, testCategoryManager



class CategoryDisplay :

    """ The table displaying the content of a CategoryManager, as a tkinter frame """

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
        self.table.bind('<<TreeviewSelect>>', self.on_select)

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
        for i, category in enumerate(self.categoryManager.categories) :
            self.table.insert(parent='', index='end', text='', values=(f"{category['name']}", f"{category['color_rgb']}", f"{i}"), tags=(f"category_{i}"))
            self.table.tag_configure(f"category_{i}", background ="#%02x%02x%02x" % tuple(category['color_rgb']))

        self.table.pack()

        self.selectedCategory = None


    def updateTable(self) :
        for row in self.table.get_children():
            self.table.delete(row)
        for i, category in enumerate(self.categoryManager.categories) :
            self.table.insert(parent='', index='end', text='', values=(f"{category['name']}", f"{category['color_rgb']}", f"{i}"), tags=(f"category_{i}"))
            self.table.tag_configure(f"category_{i}", background ="#%02x%02x%02x" % tuple(category['color_rgb']))


    def on_select(self, event):
        focus = self.table.focus()
        item = self.table.item(focus, "values")
        self.selectedCategory = self.categoryManager.categories[int(item[-1])]
        print("self.selectedCategory  :", self.selectedCategory)
        print(item)

if __name__ == "__main__" :

    window  = Tk()
    window.geometry("1000x800")
    window['bg'] = "black"

    categoryManager = testCategoryManager()

    categoryDisplay = CategoryDisplay(window, categoryManager)

    categoryDisplay.frame.place(x=300, y=20)

    window.mainloop()
