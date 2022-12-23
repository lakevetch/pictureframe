import os
import tkinter
from tkinter import *
import random as r
from PIL import Image, ImageTk
from screeninfo import get_monitors
import pickle
import valid as v
import gc

PATH = "/home/picture/Pictures/2022-Highlights"
LOOPTIME = 30

class Slideshow(Tk):
    __done = []
    __photo = ""
    __runs = 0
    __continue = True

    def __init__(self, photo_list, looptime, widths, heights):
        Tk.__init__(self)
        self.configure(bg="black")
        self.__delay = looptime * 1000
        self.__photo_list = photo_list
        self.__widths = widths
        self.__heights = heights
        self.__display = tkinter.Label(self, bg="black", image=None)
        self.__display.pack(anchor="n")
        self.__quit = tkinter.Button(self, bg="black", fg="white", text="STOP", command=self.quit_show)
        self.__quit.pack(anchor="s")
        self.__skip = tkinter.Button(self, bg="black", fg="white", text="SKIP", command=self.show_slide)
        self.__skip.pack(anchor="e")
        dimensions = str(widths[0]) + "x" + str(heights[0])
        self.geometry(dimensions)
        self.attributes("-fullscreen", True)
    
    def get_continue(self):
        return self.__continue
    
    def prep_photo(self, photo):
        """
        Readies the selected photo for display and stores it as a field of the
        Slideshow tkinter window object.
        :param photo: Image class object from PIL
        :return: None
        """
        img = self.resize_photo(photo)
        img = ImageTk.PhotoImage(img)
        self.__photo = img
    
    def quit_show(self):
        """
        Quits show by destroying the tkinter window. Program goes to menu.
        :return: None
        """
        self.destroy()
        self.__continue = False
        
    def resize_photo(self, photo):
        """
        Uses attributes of the screen being used to resize image files to
        nearly fill the screen.
        :param photo: Image class object from PIL to be resized
        :return: resized Image class object
        """
        if photo.size[0] > photo.size[1]:
            factor_w = (self.__widths[0] - self.__widths[0] / 30) / photo.size[0]
            factor_h = (self.__heights[0] - self.__widths[0] / 30) / photo.size[1]
            if factor_h > factor_w:
                factor = factor_w
            else:
                factor = factor_h
        else:
            factor = (self.__heights[0] - self.__heights[0] / 30) / photo.size[1]
        resized = photo.resize((int((photo.size[0] * factor) // 1), int((photo.size[1] * factor) // 1)))
        return resized
        
    def run(self):
        """
        Command to start the tkinter application window.
        :return: None
        """
        self.mainloop()
        
    def select_photo(self):
        """
        Algorithm to randomly select from the list of photos and
        maintain a list of completed selections in order to never double
        until all photos have been shown.
        :return: Image class object chosen from list of available objects
        """
        index = 0
        index = r.randrange(len(self.__photo_list))
        if 0 < len(self.__done) < len(self.__photo_list):
            while index in self.__done:
                index = r.randrange(len(self.__photo_list))
            self.__done.append(index)
        elif len(self.__done) == len(self.__photo_list):
            self.__done.clear()
            self.__done.append(index)
        else:
            self.__done.append(index)
        photo = self.__photo_list[index]
        return photo
    
    def show_slide(self):
        """
        Main control for slideshow. Calls all preparatory functions, prepares
        and saves an image, displays the image, and sets itself to run again
        after the preset delay period. Also creates a skip button to skip to
        the next run of the function.
        :return: None
        """
        photo = self.select_photo()
        self.prep_photo(photo)
        img = self.__photo
        self.__display.config(image=img, bg="black")
        self.after(self.__delay, self.show_slide)
        self.__runs += 1
        print(self.__runs)
        #print(dir())
        #if self.__runs == 20:
        #    self.destroy()
        

def main():
    widths = []
    heights = []
    screen_size(widths, heights)
    path = load_option("path")
    looptime = load_option("looptime")
    runs = 0
    t_main = True
    while t_main:
        if runs == 0:
            choice = 1
        else:
            choice = main_menu()
        if choice == 1:
            filename_list = load_avail_photos(path)
            photo_list = open_photos(filename_list, path)
            t_one = True
            while t_one:
                #if type(photo_list) == type("")
                show = Slideshow(photo_list, looptime, widths, heights)
                show.show_slide()
                show.run()
                t_one = show.get_continue()
        elif choice == 2:
            looptime = change_freq()
            save_option(looptime, "looptime")
        elif choice == 3:
            proceed = v.get_y_or_n("Change the path to the image folder? (y/n): ")
            if proceed == y:
                path = change_path()
                save_option(path, "path")
        elif choice == 4:
            t_main = False
        runs = 1


def change_freq():
    """
    Takes and validates user input of a new time for photos to display
    before the next photo displays.
    :return: integer, new number of seconds for photos to display
    """
    frequency = 0
    while frequency < 1:
        frequency = v.get_integer("Please enter a number of seconds: ")
        if frequency < 1:
            print("Must enter a positive non-zero number of seconds.")
    print(f"{frequency} seconds entered.")
    print()
    return frequency

    
def change_path():
    """
    Takes user input of a new path to an image folder on the local disk.
    :return: string, the path to the image folder
    """
    path = ""
    path = v.get_string("Enter path to image folder: ")
    return path


def load_avail_photos(path):
    """
    Attempts to read the directory located at the path given and list all
    files therein. If it fails it prompts the user for a new path and tries
    again until a valid path is given.
    :param path: string, path to directory where the image files are held
    :return: list of available filenames in directory at end of path
    """
    photos = []
    try:
        photos = os.listdir(path)
        return photos
    except:
        print("Invalid path.")
        path = change_path()
        photos = load_avail_photos(path)
        return photos
    

def load_option(name):
    """
    Looks for and attempts to load a previous user setting. Falls back on
    defaults if no save file is found.
    :param name: string, name of the file to look for
    :return: object, the saved option
    """
    try:
        option = pickle.load(open(name, "rb"))
        return option
    except:
        if name == "path":
            return PATH
        elif name == "looptime":
            return LOOPTIME
        
        
def main_menu():
    """
    Prints a menu of options and prompts the user to choose one, validating
    their choice.
    :return: integer, the user's chosen option
    """
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
    """
    Takes the list of filenames at path and populates a new list of PIL Image
    objects for each filename in list.
    :param filename_list: list of string filenames from the directory
    :param path: string, path to the directory
    :return: list of Image objects
    """
    photo_list = []
    try:
        for filename in filename_list:
            photo = Image.open(path + "/" + filename)
            photo_list.append(photo)
        return photo_list
    except:
        print("please update path")
#        print()
#        print("Hmm, I've run into a problem.")
#        print("Either the path to your image folder is incorrect,")
#        print("or I can't read one of the files in the folder.")
#        print("Please check that you gave the correct folder. Current path:")
#        print(f"{path}")
#        print("If that is correct, then check the folder for any non-image\n"
#              "files and remove them.")
#        print()
#        print("Then either:")
#        print("1: Enter a new path and I'll try again")
#        print("2: Just have me try it again")
#        choice = ""
#        choice = v.get_integer("Your choice: ")
#        if choice == 1:
#            path = change_path()
#            return path
#        if choice == 2:
#            photo = select_photo(photos, done, path)
#            return photo


def save_option(option, name):
    """
    Saves a user-selected option for future runs of the program by writing
    a serialized version of the object denoting the option to a file.
    :param option: object, the option to be saved
    :param name: string, the name of the option to be saved, becomes the name
    of the file
    :return: None
    """
    pickle.dump(option, open(name, "wb"))


def screen_size(widths, heights):
    """
    Uses a module to access and return the pixel dimensions of the screen the
    computer is displaying to.
    :param widths: empty list to append width to
    :param heights: empty list to append height to
    :return: None
    """
    for monitor in get_monitors():
        width = monitor.width
        height = monitor.height
        widths.append(width)
        heights.append(height)


main()