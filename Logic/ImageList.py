from GoogleApi.GoogleApi import GoogleApi
from Logic.GoogleImage import GoogleImage
import json
import random


class ImageList:
    __list = None
    __index = -1
    __focus = None

# constructors
    def __init__(self, *images):
        self.__list = []
        for img in images:
            self.__list.append(img)

    @classmethod
    def fetch_all(cls):
        tuples = GoogleApi.get_all_imgs()
        imgs = []
        if tuples:
            for t in tuples:
                imgs.append(GoogleImage(*t))
            return cls(*imgs)

    @classmethod
    def fetch_jpegs(cls):
        tuples = GoogleApi.get_all_jpegs()
        imgs = []
        if tuples:
            for t in tuples:
                imgs.append(GoogleImage(*t))
            return cls(*imgs)

    @classmethod
    def fetch_non_jpegs(cls):
        non_jpegs = GoogleApi.get_all_nonjpegs()
        imgs = []
        if non_jpegs:
            for t in non_jpegs:
                imgs.append(GoogleImage(*t))
            return cls(*imgs)

    # make iterable
    def __iter__(self):
        return self

    def __next__(self):
        self.__index += 1
        if self.__index < len(self.__list):
            return self.__list[self.__index]
        self.__index = -1
        raise StopIteration

    def __getitem__(self, index):
        return self.__list[index]

    def __len__(self):
        return len(self.__list)

    def append(self, img):
        self.__list.append(img)

    def pop(self, index):
        self.__list.pop(index)

# accessors
    def get_list(self):
        return list(self.__list)

    def get_focus(self):
        return self.__focus

# mutators
    def set_list(self, iterable):
        self.__list = list(iterable)

    def set_focus(self, focus):
        self.__focus = focus

# utils
    def get_json_uris(self, uri_type):
        uris = []
        for img in self:
            if uri_type == 'view':
                uris.append(img.gen_view_uri())
            elif uri_type == 'download':
                uris.append(img.get_download_uri())
        return json.dumps(uris)

    def convert_all(self):
        for img in self:
            if img.get_mime_type() != 'image/jpeg':
                img.conversion_flow()

    def get_name_list(self):
        name_list = []
        for img in self:
            name_list.append(img.get_name())
        return name_list

    def get_orientations(self):
        orientations = []
        for img in self:
            orientations.append(img.get_orientation())
        return orientations

    def random_focus(self):
        self.__focus = self.__list.index(random.choice(self.__list))


# debug/test block
if __name__ == '__main__':
    img_list = ImageList.fetch_jpegs()
    img_list.random_focus()
    print(img_list.get_focus())
