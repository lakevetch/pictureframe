from pathlib import Path


class Project:
    __ROOT_PATH = None
    __OAUTH_PATH = None
    __IMG_PASSTHRU_PATH = None
    __STATIC_PATH = None

    def __init__(self, root_pathname):
        self.__ROOT_PATH = Path(root_pathname)
        self.__STATIC_PATH = self.__ROOT_PATH / 'static'
        self.__OAUTH_PATH = self.__STATIC_PATH / 'credentials.json'
        self.__IMG_PASSTHRU_PATH = self.__STATIC_PATH / 'img_passthru'

    def get_root(self):
        return self.__ROOT_PATH

    def get_static(self):
        return self.__STATIC_PATH

    def get_oauth(self):
        return self.__OAUTH_PATH

    def get_img_passthru(self):
        return self.__IMG_PASSTHRU_PATH
