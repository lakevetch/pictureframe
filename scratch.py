import os
import tkinter
from tkinter import *
import random as r
from PIL import Image, ImageTk
from screeninfo import get_monitors
#from itertools import cycle
import subprocess

import valid as v

PATH = "/home/picture/Pictures"
LOOPTIME = 5

class Slideshow(Tk):
    __done = []

    def __init__(self, photo_list, looptime, widths, heights):
        Tk.__init__(self)
        self.__delay = looptime * 1000
        self.__photo_list = self.prep_photos(photo_list)
        self.__photo_list = cycle((tkinter.PhotoImage(file=image), image) for image in photo_list)
        self.__display = tkinter.Label(self, bg="black")
        self.__display.pack(anchor="n")
        self.__quit = tkinter.Button(self, bg="black", fg="white", text="STOP", command=self.quit_show)
        self.__skip = rkinter.Button(self, b"black", fg="white", text="SKIP", command=self.show_slide)
        dimensions = str(widths[0]) + "x" + str(heights[0])
        self.geometry(dimensions)
        #self.after(0, self.show_slide)
    
    def quit_show(self):
        self.destroy()
        
    def run(self):
        self.mainloop()
        
    def select_photo(self):
        index = 0
        index = r.randrange(len(self.__photo_list))
        if len(self.__done) > 0:
            while index in self.__done:
                index = r.randrange(len(self.__photo_list))
            self.__done.append(index)
        elif len(self.__done) == len(self.__photo_list):
            self.__done.clear()
            self.__done.append(index)
        else:
            self.__done.append(index)
        photo = self.__photo_list
        return photo
    
    def show_slide(self):
        #img = self.select_photo()
        img = next(self.__photo_list)
        self.__display.config(image=img)
        self.after(self.__delay, self.slideshow)
        
    def prep_photos(self, photo_list):
        new_list = []
        for photo in photo_list:
            new = tkinter.PhotoImage(file=photo)
            new_list.append(new)
        return new_list
        
    


def main():
    widths = []
    heights = []
    screen_size(widths, heights)
    path = PATH
    looptime = LOOPTIME
    runs = 0
    t_main = True
    while t_main:
        if runs == 0:
            choice = 1
        else:
            choice = main_menu()
        if choice == 1:
            filename_list = load_avail_photos(path)
            #convert_photos(filename_list, path)
            #photo_list = open_photos(filename_list, path)
            #photo_list = resize_photos(photo_list, widths, heights)
            show = Slideshow(filename_list, looptime, widths, heights)
            show.show_slide()
            show.run()
                
    
    
    
def load_avail_photos(path):
    photos = []
    try:
        photos = os.listdir(path)
        return photos
    except:
        print("Invalid path.")
        path = change_path()
        photos = load_avail_photos(path)
        return photos
    
    
def change_path():
    path = ""
    path = v.get_string("Enter path to image folder: ")
    return path


def resize_photos(photos, widths, heights):
    resized = []
    for photo in photos:
        if photo.size[0] > photo.size[1]:
            factor_w = widths[0] / photo.size[0]
            factor_h = heights[0] / photo.size[1]
            if factor_h > factor_w:
                factor = factor_w
            else:
                factor = factor_h
        else:
            factor = heights[0] / photo.size[1]
        new = photo.resize((int((photo.size[0] * factor) // 1), int((photo.size[1] * factor) // 1)))
        resized.append(new)
    return resized


def screen_size(widths, heights):
    for monitor in get_monitors():
        width = monitor.width
        height = monitor.height
        widths.append(width)
        heights.append(height)
    
    
def main_menu():
    print()
    print("1: Start the slideshow!")
    print("2: Change cycle frequency (default 30 seconds)")
    print("3: Advanced configuration")
    print("4: Quit")
    print()
    choice = 0
    while not choice in range(1, 5):
        choice = v.get_integer("Please enter a menu option: ")
    return choice


def open_photos(filename_list, path):
    photo_list = []
    for filename in filename_list:
        photo = Image.open(path + "/" + filename)
        photo_list.append(photo)
    return photo_list


def convert_photos(filename_list, path):
    new_list = []
    for name in filename_list:
        split = name.rsplit(".")
        stripped = split[0]
        full_stripped = path + "/" + stripped
        command = "bash -c 'convert \"" + path + "/" + name + " \"" + full_stripped + ".gif\"'"
        subprocess.call([command])
        


main()