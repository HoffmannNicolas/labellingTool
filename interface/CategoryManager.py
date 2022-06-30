
import json
from os.path import exists

class CategoryManager :

    """ Manages all categories shared between all objects of the interface """

    def __init__(self, categories=[]) :
        self.selectedCategory = None
        self.categories = categories


    def addCategory(self, category) :
        self.categories.append(category)


    def loadFromFolder(self, folderPath) :
        saveFile = f"{folderPath}/CategoryManager.json"
        if exists(saveFile) :
            with open(saveFile) as file :
                self.categories = json.loads(file.read())
        else :
            self.saveToFolder(folderPath)


    def saveToFolder(self, folderPath) :
        saveFile = f"{folderPath}/CategoryManager.json"
        with open(saveFile, 'w') as file :
            json.dump(self.categories, file, indent=4)


    def __str__(self) :
        toPrint = f"CategoryManager :\n"
        for i, category in enumerate(self.categories) :
            toPrint += f"\t[{i}] : {category}\n"
        return toPrint


def testCategoryManager() :
    categoryManager = CategoryManager()
    categoryManager.addCategory({"name" : "Cat", "color_rgb" : [200, 200, 0]})
    categoryManager.addCategory({"name" : "Human", "color_rgb" : [230, 120, 0]})
    categoryManager.addCategory({"name" : "Robot", "color_rgb" : [100, 100, 100]})
    categoryManager.addCategory({"name" : "Overlord", "color_rgb" : [60, 60, 100]})
    categoryManager.addCategory({"name" : "Snowboard", "color_rgb" : [230, 230, 255]})
    categoryManager.addCategory({"name" : "Sun", "color_rgb" : [255, 255, 180]})
    categoryManager.addCategory({"name" : "Lava", "color_rgb" : [200, 60, 0]})
    categoryManager.addCategory({"name" : "Water", "color_rgb" : [110, 110, 200]})
    categoryManager.addCategory({"name" : "Tree", "color_rgb" : [20, 80, 20]})
    categoryManager.addCategory({"name" : "Dispear", "color_rgb" : [666, 666, 666]})
    categoryManager.addCategory({"name" : "Git", "color_rgb" : [0, 0, 0]})
    categoryManager.addCategory({"name" : "Catpuccino", "color_rgb" : [255, 220, 20]})
    return categoryManager


if __name__ == "__main__" :

    categoryManager = testCategoryManager()

    categoryManager.saveToFolder("./data")
    categoryManager2 = CategoryManager()
    categoryManager2.loadFromFolder("./data")
    print(categoryManager2)
