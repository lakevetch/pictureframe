from Logic.ImageList import ImageList


class Slideshow(ImageList):
    __slides = None
    __timeout = None
    __play = True

    def __init__(self, *slides, timeout=17):
        super().__init__(*slides)
        self.__slides = slides
        self.__timeout = timeout

    # def play(self):
    #     while self.__play:
    #
    # def next(self):

