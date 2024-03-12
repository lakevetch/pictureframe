from googleapiclient.discovery import build
from google.auth import default
import google.auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = '1hPJkFLpcrqhrUCnWrYW7JbAvaQ-HZd23'


class GoogleApi:
    __service = None
    __drive = None
    __files = None
    __path_constants = None
    __fields = 'id', 'name', 'mimeType', 'webContentLink', 'imageMediaMetadata', 'md5Checksum'
    __headers = 'sec-fetch-mode: no-cors'

    @classmethod
    def connect(cls):
        if not cls.__service:
            cls.__service = cls.get_gdrive_service()
            cls.__drive = cls.__service.drives()
            cls.__files = cls.__service.files()

    @classmethod
    def load_key(cls):
        creds = google.auth.load_credentials_from_file('../credentials.json', scopes=SCOPES)[0]
        return creds

    @classmethod
    def get_gdrive_service(cls):
        credentials = cls.load_key()
        return build('drive', 'v3', credentials=credentials)

    @classmethod
    def list_files(cls, query_str='', fields=None):
        cls.connect()
        request = cls.__files.list(q=query_str, fields=fields)
        print(request.execute()['files'])

    @classmethod
    def list_folders(cls, query_str=''):
        cls.connect()
        query = "mimeType='application/vnd.google-apps.folder' " + query_str
        request = cls.__files.list(q=query)
        print(request.execute()['files'])

    @classmethod
    def get_file_by_id(cls, file_id):
        cls.connect()
        request = cls.__files.get(fileId=file_id, alt='media', fields='*')
        response = request.execute()
        if response:
            file_tuple = tuple(response[field] for field in cls.__fields)
            return file_tuple

    @classmethod
    def get_all_imgs(cls):
        return cls.get_imgs(f"'{FOLDER_ID}' in parents")

    @classmethod
    def get_all_jpegs(cls):
        return cls.get_imgs(f"'{FOLDER_ID}' in parents and mimeType='image/jpeg'")

    @classmethod
    def get_all_nonjpegs(cls):
        return cls.get_imgs(f"'{FOLDER_ID}' in parents and mimeType!='image/jpeg'")

    @classmethod
    def get_imgs(cls, body):
        cls.connect()
        request = cls.__files.list(fields='*', q=body)
        response = request.execute()
        if response:
            tuples = []
            for item in response['files']:
                file_tuple = tuple(item[field] for field in cls.__fields)
                tuples.append(file_tuple)
            return tuples

    @classmethod
    def delete_img(cls, img_id):
        cls.connect()
        request = cls.__files.delete(fileId=str(img_id))
        response = request.execute()
        if response:
            print(f'{img_id} not deleted.')
        else:
            print(f'{img_id} deleted successfully.')

    @classmethod
    def upload_img(cls, img, body):
        cls.connect()
        body['parents'] = [f'{FOLDER_ID}']
        request = cls.__files.create(uploadType='media', media_body=img, body=body)
        request.execute()


if __name__ == '__main__':
    print(GoogleApi.load_key())
