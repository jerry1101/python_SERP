import gspread

from oauth2client import file, client, tools
from apiclient import discovery
from httplib2 import Http


def get_sheets_client():
    creds = __get_credential()
    return gspread.authorize(creds)


def __get_credential():

    _SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    store = file.Storage('storage.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', _SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


def get_sheets_resource():
    sheet_credential = __get_credential()
    return discovery.build('sheets', 'v4', http=sheet_credential.authorize(Http()))

