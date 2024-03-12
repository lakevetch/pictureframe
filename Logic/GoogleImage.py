import os
from Data.GoogleApi import GoogleApi
import requests
from PIL import Image
from pillow_heif import register_heif_opener
from Logic.Project import Project
from googleapiclient.http import MediaFileUpload


class GoogleImage:
    __id = None
    __name = None
    __mime_type = None
    __download_uri = None
    __width = None
    __height = None
    __orientation = None
    __hash_code = None
    __img = None
    __path_const = None

# constructors
    def __init__(self, drive_id, name, mime_type, uri, metadata_dict, hash_code):
        self.__id = drive_id
        self.__name = name
        self.__mime_type = mime_type
        self.__download_uri = uri
        self.__width = metadata_dict['width']
        self.__height = metadata_dict['height']
        if self.__width > self.__height:
            self.__orientation = 'landscape'
        else:
            self.__orientation = 'portrait'
        self.__hash_code = hash_code
        self.__path_const = Project('C:/Users/Jack/Desktop/pythonsketchbook/pictureframe')

    @classmethod
    def fetch_by_id(cls, drive_id):
        img_tuple = GoogleApi.get_file_by_id(drive_id)
        if img_tuple:
            return cls(*img_tuple)

# accessors
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_mime_type(self):
        return self.__mime_type

    def get_download_uri(self):
        return self.__download_uri

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_orientation(self):
        return self.__orientation

    def get_img(self):
        return self.__img

    def get_hash(self):
        return self.__hash_code

# mutators
    def set_id(self, drive_id):
        self.__id = drive_id

    def set_name(self, name):
        self.__name = name

    def set_mime_type(self, mime_type):
        self.__mime_type = mime_type

    def set_uri(self, uri):
        self.__download_uri = uri

    def set_width(self, width):
        self.__width = int(width)

    def set_height(self, height):
        self.__height = int(height)

    def set_orientation(self, orientation):
        if orientation in ('portrait', 'landscape'):
            self.__orientation = orientation

    def set_hash(self, hash_code):
        self.__hash_code = hash_code

# utils
    def __str__(self):
        string = f'Image object--\n'\
                 f'  Id: {self.__id}\n'\
                 f'  Name: {self.__name}\n' \
                 f'  Mime type: {self.__mime_type}\n'\
                 f'  Download link: {self.__download_uri}\n'
        return string

    def __eq__(self, other):
        return self.__hash_code == other.__hash_code

    def conversion_flow(self): # this could likely be made more efficient
        from Logic.ImageList import ImageList
        self.convert_to_jpg()
        if self.__name not in tuple(img.get_name() for img in ImageList.fetch_jpegs()):
            self.upload()
        self.delete_locally()
        self.delete_from_drive()

    def convert_to_jpg(self):
        if self.__mime_type != 'image/jpeg':
            register_heif_opener()
            if not self.__img:
                self.download()
            self.__img = self.__img.convert('RGB')
            name_bits = self.__name.split('.')
            name_bits.pop(-1)
            new_name = ''
            for bit in name_bits:
                new_name += bit + '.'
            new_name += 'jpg'
            os.remove(self.__name)
            self.__img.save(new_name)
            self.__name = new_name
            self.__mime_type = 'image/jpeg'

    def delete_from_drive(self):
        GoogleApi.delete_img(self.__id)

    def delete_locally(self):
        # os.chdir(self.__path_const.get_img_passthru())
        os.remove(self.__name)

    def download(self):
        register_heif_opener()
        # os.chdir(self.__path_const.get_img_passthru())
        r = requests.get(self.__download_uri)
        if r:
            file = open(self.__name, 'wb')
            file.write(r.content)
            self.__img = Image.open(self.__name)

    def gen_view_uri(self):
        return f'https://lh3.google.com/u/0/d/{self.__id}'

    def to_dict(self):
        return {
            'id': self.__id,
            'name': self.__name,
            'mimeType': self.__mime_type
        }

    def upload(self):
        if self.__img:
            # uploadable = MediaFileUpload(os.path.join(self.__path_const.get_img_passthru(), self.__name))
            uploadable = MediaFileUpload(self.__name)
            GoogleApi.upload_img(uploadable, {'name': self.__name})


if __name__ == '__main__':
    img = GoogleImage.fetch_by_id('1O86hK4up3I1yZMmeCwRGSKX7at3vNDkI')
    img.conversion_flow()