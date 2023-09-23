from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from display.models import Club

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '13LE0EJ3JziGz_ISYmr1eNyoDln-EeFBFWXUbeE-TbQc'
SAMPLE_RANGE_NAME = 'Form Responses 1!B1:F50'

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to credentials.json
credentials_path = os.path.join(script_dir, 'credentials.json')

token_path = os.path.join(script_dir, "token.json")

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(token_path)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())\
    
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
            club_name = row[0]
            first_name = row[1]
            last_name = row[2]
            description = row[4]

            # reformat the data according to your rules
            if '/' in first_name:
                # Split first_name and last_name by "/"
                first_name_parts = first_name.split('/')
                last_name_parts = last_name.split('/')

                # Construct leaders string
                leaders = first_name_parts[0] + " " + last_name_parts[0] + ", " + first_name_parts[1] + " " + last_name_parts[1]

                email = first_name_parts[0][0] + last_name_parts[0] + "@cannonschool.org"

            else:
                leaders = first_name + " " + last_name # concatenate first and last name

                email = first_name[0] + last_name + "@cannonschool.org"
                email = email.lower()
                
            # create a new club instance and save it
            if " " in email:
                del email
                club = Club(name=club_name, leaders=leaders, description=description)
                club.save()
                continue
            club = Club(name=club_name, leaders=leaders, description=description, emails = email)
            club.save()
        
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()

        
        
