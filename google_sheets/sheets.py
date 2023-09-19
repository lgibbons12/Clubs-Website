from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from display.models import Club

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '13LE0EJ3JziGz_ISYmr1eNyoDln-EeFBFWXUbeE-TbQc'
SAMPLE_RANGE_NAME = 'Form Responses 1!B1:F50'

copied_json = '''{"installed":{"client_id":"575384953477-malautubclfmdifudod610bmqn50jrcf.apps.googleusercontent.com","project_id":"cannon-clubs-scraping","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}'''

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create credentials from the provided JSON data
            creds = Credentials.from_authorized_user_info(
                json.loads(copied_json), scopes=SCOPES
            )
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return
        
        # loop through the values and save them into the model
        for row in values[1:]: # skip the header row
            # extract the data from each row
            club_name = row[1]
            first_name = row[2]
            last_name = row[3]
            description = row[5]

            # reformat the data according to your rules
            if '/' in first_name:
                # Split first_name and last_name by "/"
                first_name_parts = first_name.split('/')
                last_name_parts = last_name.split('/')

                # Construct leaders string
                leaders = first_name_parts[0] + " " + last_name_parts[0] + ", " + first_name_parts[1] + " " + last_name_parts[1]
            else:
                leaders = first_name + " " + last_name # concatenate first and last name

            # create a new club instance and save it
            club = Club(name=club_name, leaders=leaders, description=description)
            club.save()
        
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
