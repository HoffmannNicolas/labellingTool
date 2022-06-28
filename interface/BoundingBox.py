

class BoundingBox :


    """ A bounding box is a rectangle containing a labeled object """


    def __init__(self, left_percentage, top_percentage, right_percentage, bottom_percentage, category) :

        """ Coordinates of the rectangle (top-right-bottom-left) are in percentage of the width and height """

        self.left_percentage = left_percentage
        self.top_percentage = top_percentage
        self.right_percentage = right_percentage
        self.bottom_percentage = bottom_percentage

        self.category = category
