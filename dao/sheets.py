from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path


class SheetService:
    def __init__(self):
        self.__creds = None
        self.__credential_path = 'dao/credentials/credentials.json'
        self.__prepare_credentials()
        self.service_name = 'sheets'
        self.version = 'v4'
        self.__service = self.__setup_service()

    def __prepare_credentials(self):
        assert self.__credential_path is not None

        if os.path.exists('dao/credentials/token.pickle'):
            with open('dao/credentials/token.pickle', 'rb') as token:
                self.__creds = pickle.load(token)

        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=self.__credential_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
                self.__creds = flow.run_local_server(port=0)

        with open('dao/credentials/token.pickle', 'wb') as token:
            pickle.dump(self.__creds, token)

    def __setup_service(self):
        assert self.__creds is not None
        return build(serviceName=self.service_name,
                     version=self.version,
                     credentials=self.__creds)

    def get(self, spread_sheet_id=None):
        assert spread_sheet_id is not None
        sheet = self.__service.spreadsheets()

        # get the latest sheet
        sheet_metadata = sheet.get(spreadsheetId=spread_sheet_id).execute()
        sheet_name = (sheet_metadata['sheets'][0]['properties']['title'])
        result = sheet.values().get(spreadsheetId=spread_sheet_id,
                                    range=sheet_name).execute()
        return result.get('values', [])
