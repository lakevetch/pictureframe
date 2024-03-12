from pymongo import MongoClient


class MongoDB:
    __images = None
    __timeouts = None
    __tokens = None
    __collections = None
    __client = None
    __database = None

    @classmethod
    def connect(cls):
        if not cls.__client:
            uri = "mongodb+srv://jjacksanders:picture_frame_password@cluster0.mpkxy4u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            cls.__client = MongoClient(uri)
            cls.__database = cls.__client.PictureFrame
            cls.__images = cls.__database.Images
            cls.__timeouts = cls.__database.Timeouts
            cls.__tokens = cls.__database.Tokens
            cls.__collections = cls.__images, cls.__timeouts, cls.__tokens
            print(cls.__collections)


if __name__ == '__main__':
    MongoDB.connect()
