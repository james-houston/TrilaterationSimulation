from random import randint


class Beacon:

    def __init__(self,x=None,y=None,height=1000,width=1000):
        minHeight = int(0.1*height)
        maxHeight = int(0.9*height)
        minWidth = int(0.1*width)
        maxWidth = int(0.9*width)

        if not x:
            self.x = randint(minWidth,maxWidth)
        else:
            self.x = x
        if not y:
            self.y = randint(minHeight,maxHeight)
        else:
            self.y = y
