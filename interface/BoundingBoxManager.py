
from os.path import exists, isdir

from random import randint, uniform
from random import randint
from CategoryManager import CategoryManager, testCategoryManager

import json


class BoundingBoxManager :


    """ Manages all the bounding boxes, shared between all elements of the interface """


    def __init__(self) :
        self.boundingBoxes = {}


    def addBoundingBox(self, imagePath, left, top, right, bottom, category=None) :
        if (imagePath not in list(self.boundingBoxes.keys())) :
            self.boundingBoxes[imagePath] = []
        self.boundingBoxes[imagePath].append({
            "left_percentage" : left,
            "top_percentage" : top,
            "right_percentage" : right,
            "bottom_percentage" : bottom,
            "category" : category
        })


    def loadFromFolder(self, folderPath) :
        saveFile = f"{folderPath}/BoundingBoxManager.json"
        if exists(saveFile) :
            with open(saveFile) as file :
                self.boundingBoxes = json.loads(file.read())
        else :
            if (isdir(folderPath)) :
                self.saveToFolder(folderPath)


    def saveToFolder(self, folderPath) :
        if (isdir(folderPath)) :
            saveFile = f"{folderPath}/BoundingBoxManager.json"
            with open(saveFile, 'w') as file :
                json.dump(self.boundingBoxes, file, indent=4)


    def __str__(self) :
        toPrint = "BoundingBoxManager\n"
        for imagePath in self.boundingBoxes.keys() :
            toPrint += f"\t['{imagePath}']\n"
            for i, bbox in enumerate(self.boundingBoxes[imagePath]) :
                toPrint += f"\t\t[{i}] : {bbox}\n"
        return toPrint



if __name__ == "__main__" :

    categoryManager = testCategoryManager()


    bboxManager = BoundingBoxManager()
    for _ in range(10) :
        category = categoryManager.categories[randint(0, len(categoryManager.categories)) - 1]
        bboxManager.addBoundingBox("imagePath", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=category)

    for _ in range(10) :
        bboxManager.addBoundingBox("imagePath2", uniform(0, 100), uniform(0, 100), uniform(0, 100), uniform(0, 100), category=categoryManager.categories[0])

    bboxManager.saveToFolder("./data")
    bboxManager2 = BoundingBoxManager()
    bboxManager2.loadFromFolder("./data")

    print(bboxManager2)
