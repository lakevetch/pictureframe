import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path
from Logic.Project import Project

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = '1hPJkFLpcrqhrUCnWrYW7JbAvaQ-HZd23'


class GoogleApi:
    __service = None
    __drive = None
    __files = None
    __path_constants = None
    __fields = 'id', 'name', 'mimeType', 'webContentLink', 'imageMediaMetadata', 'md5Checksum'

    @classmethod
    def connect(cls):
        if not cls.__path_constants:
            cls.__path_constants = Project('C:/Users/Jack/Desktop/pythonsketchbook/pictureframe')
        if not cls.__service:
            cls.__service = cls.get_gdrive_service()
            cls.__drive = cls.__service.drives()
            cls.__files = cls.__service.files()

    @classmethod
    def get_gdrive_service(cls):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        os.chdir(cls.__path_constants.get_static())
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cls.__path_constants.get_oauth(), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)

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
        cls.connect()
        request = cls.__files.list(fields='*', q=f"'{FOLDER_ID}' in parents")
        response = request.execute()
        if response:
            tuples = []
            for item in response['files']:
                file_tuple = tuple(item[field] for field in cls.__fields)
                tuples.append(file_tuple)
            return tuples

    @classmethod
    def get_all_jpegs(cls):
        cls.connect()
        request = cls.__files.list(fields='*', q=f"'{FOLDER_ID}' in parents and mimeType='image/jpeg'")
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
        response = request.execute()


if __name__ == '__main__':
    # print(GoogleApi.list_files())
    # print(GoogleApi.get_file_by_id('1XqdKe-keuwZ0LTJxLMlfQFRaI7SOCyxG'))
    GoogleApi.list_files(query_str=f"'{FOLDER_ID}' in parents", fields='*')
    # for item in GoogleApi.get_file_by_id('1O86hK4up3I1yZMmeCwRGSKX7at3vNDkI'):
    #     print(item)
