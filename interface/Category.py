

class Category :


    """ A categry, or class, caracterises the object inside a bounding box """


    def __init__(self, name="Category", color_rgb=[255, 255, 255]) :

        """ The color of the class is saved as RGB and can be accessed as hexa """

        self.name = name
        self.color_rgb = color_rgb


    def getColor_hexa(self) :

        """ Transforms RGB values in hexa """

        return "#%02x%02x%02x" % self.color_rgb
