import os
import tkinter
from tkinter import *
import random as r
from PIL import Image, ImageTk
from screeninfo import get_monitors
from itertools import cycle

import valid as v

PATH =
LOOPTIME = 30

class Slideshow(Tk):

    def __init__(self, photo_list, looptime):
        Tk.__init__(self)
        self.__delay = looptime
        self.__photo_list = cycle(tkinter.PhotoImage(file=image), image), for image in photo_list)


