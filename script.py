import os.path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
  try:
    drive = get_driver_service()
    list_files(drive)
  except HttpError as error:
    print(f'An error occurred: {error}')

def get_driver_service():
  credentials = setup_credentials()
  drive = build('drive', 'v3', credentials=credentials)

  return drive

def setup_credentials():
  credentials = get_credentials_from_local_file()

  if not credentials:
    credentials = get_user_authorization()
  elif can_user_refresh_token(credentials):
    credentials = refresh_token()

  write_credentials_to_the_local_file(credentials)

  return credentials
  
def get_credentials_from_local_file():
  credentials = None

  if os.path.exists('token.json'):
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

  return credentials

def get_user_authorization():
  if not os.path.exists('credentials.json'):
    raise Exception('Credentials file does not exist.')

  flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

  return  flow.run_local_server()

def can_user_refresh_token(credentials: Credentials):
  return not credentials.valid and credentials.expired and credentials.refresh_token

def refresh_token(credentials: Credentials):
  request = Request()
  credentials.refresh(request)

def write_credentials_to_the_local_file(credentials: Credentials):
  with open('token.json', 'w') as token:
    token.write(credentials.to_json())

def list_files(drive_service):
  results = drive_service.files().list(fields="files(id, name)").execute()
  items = results.get('files', [])

  if not items:
    print('No files found.')

  for item in items:
    print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
  main()
