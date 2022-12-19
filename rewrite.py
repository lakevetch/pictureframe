import os
import tkinter
from tkinter import *
import random as r
from PIL import Image, ImageTk
from screeninfo import get_monitors

import valid as v

#import pickle
#import time

PATH = "/home/picture/Pictures"
LOOPTIME = 5


#class Backdrop:
#    def __init__(self, widths, heights):
#        self.root = Tk()
#        self.root.configure(bg="black")
#        display = ImageTk.PhotoImage(photo)
#        label = tkinter.Label(image=display)
#        label.image = display
#        label.pack()
        # self.root.attributes("-fullscreen", True)
#        self.root.after((LOOPTIME + 1) * 1000, lambda: self.root.destroy())
        #    skip_button = Button(root, text="Skip", command=root.destroy)
        #    skip_button.pack(side=RIGHT)
#        dimensions = str(widths[0]) + "x" + str(heights[0])
#        self.root.geometry(dimensions)
#        self.display_loop(photo, widths, heights)
#        self.root.mainloop()

#    def display_loop(self, photo, widths, heights):
#        done = []
#        end = time.time()
#        while True:
#            if time.time() > end:
#                photos = load_avail_photos()
#                remove_done(photos, done)
#                if len(photos) == 0:
#                    photos = load_avail_photos()
#                    done.clear()
#                photo = select_photo(photos, done)
#                photo = prep_photo(photo, widths, heights)
#                end = delay()
#                display = Display(photo, widths, heights, self)



class Display:
    __continue = True
    __duration = 0
    __photo = 0
    __label = 0
    __root = 0

    def __init__(self, photo, widths, heights, looptime, photos, path, done):
        self.__photo = photo
        self.__duration = looptime * 1000
        root = Tk()
        self.__root = root
        self.__root.configure(bg="black")
        self.__root.after(self.__duration, lambda: self.new_photo(photos, done, path, widths, heights))
        button = Button(self.__root, text="STOP", bg="black", fg="white", command=self.quit_show)
        #skip = Button(self.root, text="SKIP PHOTO", bg="black", fg="white", command=self.new_photo(photos, done, path))
        display = ImageTk.PhotoImage(self.__photo)
        self.__label = tkinter.Label(self.__root)
        self.__label.config(image=display)
        self.__label.pack(anchor="n")
        button.pack(anchor="s")
        #skip.pack(anchor="e")
        #self.__root.attributes("-fullscreen", True)
        #    skip_button = Button(root, text="Skip", command=root.destroy)
        #    skip_button.pack(side=RIGHT)
        dimensions = str(widths[0]) + "x" + str(heights[0])
        self.__root.geometry(dimensions)
        self.__root.mainloop()

    def quit_show(self):
        self.__root.destroy()
        self.__continue = False

    def quit_query(self):
        return self.__continue
    
    def new_photo(self, photos, done, path, widths, heights):
        photos = load_avail_photos(path)
        remove_done(photos, done)
        if len(photos) == 0:
            photos = load_avail_photos(path)
            done.clear()
        photo = select_photo(photos, done, path)
        photo = prep_photo(self.__photo, widths, heights)
        self.__photo = photo
        display = ImageTk.PhotoImage(self.__photo)
        self.__label.config(image=display)
        self.__root.after(self.__duration, lambda: self.new_photo(photos, done, path, widths, heights))
        


def main():
    photos = []
    done = []
    widths = []
    heights = []
    path = PATH
    looptime = LOOPTIME
    screen_size(widths, heights)
    t_main = True
    runs = 0
    while t_main:
        if runs == 0:
            choice = 1
        else:
            choice = main_menu() 
    #    end = time.time()
    #    backdrop = Backdrop(widths, heights)
    #    backdrop = create_backdrop()
        if choice == 1:
            t_one = True
            while t_one:
        #        if time.time() > end:
                photos = load_avail_photos(path)
                remove_done(photos, done)
                if len(photos) == 0:
                    photos = load_avail_photos(path)
                    done.clear()
                photo = select_photo(photos, done, path)
                if type(photo) == type(""):
                    path = photo
                    photos = load_avail_photos(path)
                    done.clear()
                    photo = select_photo(photos, done, path)
                photo = prep_photo(photo, widths, heights)
        #            end = delay()
                display = Display(photo, widths, heights, looptime, photos, path, done)
                t_one = display.quit_query()
        if choice == 2:
            looptime = change_freq()
        if choice == 3:
            cont = ""
            cont = valid.get_y_or_n("Change path to image folder? (y/n): ")
            if cont == "y":
                path = change_path()
        if choice == 4:
            t_main = False
        runs += 1
#    if choice == 2:

#        float_photo(photo, backdrop)


def load_avail_photos(path):
    photos = []
#    try:
#        photos = pickle.load(open("list", "rb"))
#    except:
#        photos = os.listdir(PATH)
#    if len(photos) == 0:
    try:
        photos = os.listdir(path)
        return photos
    except:
        print("Invalid path.")
        path = change_path()
        load_avail_photos(path)
        return path


def select_photo(photos, done, path):
    try:
        index = 0
        index = r.randrange(len(photos))
        photo = ""
        photo = Image.open(path + "/" + photos[index])
    #    pickle.dump(photo, open("most_recent", "wb"))
        done.append(photos[index])
        return photo
    except:
        print()
        print("Hmm, I've run into a problem.")
        print("Either the path to your image folder is incorrect,")
        print("or I can't read one of the files in the folder.")
        print("Please check that you gave the correct folder. Current path:")
        print(f"{path}")
        print("If that is correct, then check the folder for any non-image files\n"
              "and remove them.")
        print()
        print("Then either:")
        print("1: Enter a new path and I'll try again")
        print("2: Just have me try it again")
        choice = ""
        choice = v.get_integer("Your choice: ")
        if choice == 1:
            path = change_path()
            return path
        if choice == 2:
            photo = select_photo(photos, done, path)
            return photo


def prep_photo(photo, widths, heights):
    if photo.size[0] > photo.size[1]:
        factor_w = (widths[0] - widths[0] / 30) / photo.size[0]
        factor_h = (heights[0] - widths[0] / 30) / photo.size[1]
        if factor_h > factor_w:
            factor = factor_w
        else:
            factor = factor_h
    else:
        factor = (heights[0] - heights[0] / 30) / photo.size[1]
    resized = photo.resize((int((photo.size[0] * factor) // 1), int((photo.size[1] * factor) // 1)))
#        if resized.size[0] > 1000 or resized.size[1] > 563:
#            diff_w = resized.size[0] - 1000
#            diff_h = resized.size[1] - 563
#            if diff_w > diff_h:
#                factor = resized.size[0] / 1000
#            else:
#                factor = resized.size[1] / 563
#            resized = resized.resize((int((resized.size[0] * factor) // 1), int((resized.size[1] * factor) // 1)))
    return resized


def prep_photos(photos, widths, heights):
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


#def display_photo(photo, widths, heights):
#    dimensions = ""
#    root = Tk()
#    root.configure(bg="black")
#    display = ImageTk.PhotoImage(photo)
#    label = tkinter.Label(image=display)
#    label.image = display
#    label.pack()
#    root.attributes("-fullscreen", True)
#    root.after((LOOPTIME + 1) * 1000, lambda: root.destroy())
#    skip_button = Button(root, text="Skip", command=root.destroy)
#    skip_button.pack(side=RIGHT)
#    dimensions = str(widths[0]) + "x" + str(heights[0])
#    root.geometry(dimensions)
#    root.mainloop()


def screen_size(widths, heights):
    for monitor in get_monitors():
        width = monitor.width
        height = monitor.height
        widths.append(width)
        heights.append(height)

#def end_loop():
#    return False

#def float_photo(photo, backdrop):
#    root = Toplevel(backdrop)
#    root.configure(bg="black")
#    display = ImageTk.PhotoImage(photo)
#    label = tkinter.Label(image=display)
#    label.image = display
#    label.pack()
#    root.attributes("-fullscreen", True)
#    root.after(LOOPTIME * 1000, lambda: root.destroy())
#    skip_button = Button(root, text="Skip", command=root.destroy)
#    skip_button.pack(side=RIGHT)
#    root.geometry("1000x563")
#    root.mainloop()



#def save_state(photos, photo):
#    pickle.dump(photos, open("list", "wb"))
#    try:
#        previous = pickle.load(open("most_recent", "rb"))
#        previous.Image.close()
#    except:
#        print("Not closed")
#        return


#def delay():
#    end = time.time() + LOOPTIME
#    return end

def remove_done(photos, done):
    for name in done:
        index = photos.index(name)
        photos.pop(index)

#def create_backdrop():
#    backdrop = Tk()
#    backdrop.configure(bg="black")
#    backdrop.geometry("1000x563")
#    return backdrop

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


def change_freq():
    frequency = 0
    while frequency < 1:
        frequency = v.get_integer("Please enter a number of seconds: ")
        if frequency < 1:
            print("Must enter a positive non-zero number of seconds.")
    print(f"{frequency} seconds entered.")
    print()
    return frequency


def change_path():
    path = ""
    path = v.get_string("Enter path to image folder: ")
    return path


main()

