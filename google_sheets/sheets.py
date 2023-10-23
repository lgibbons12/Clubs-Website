from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
link = 'https://docs.google.com/spreadsheets/d/13LE0EJ3JziGz_ISYmr1eNyoDln-EeFBFWXUbeE-TbQc/edit#gid=391256049'
parts = link.split("/")
good_part = parts[5]

sheet_id = good_part
range_name = 'Form Responses 1!B1:F50'

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to credentials.json
credentials_path = os.path.join(script_dir, 'credentials.json')

token_path = os.path.join(script_dir, "token.json")

service_path = os.path.join(script_dir, 'clubs_key.json')


def main(sheet = None, dfy = False, testing_link = False):
    

    parts = sheet.split("/")
    id = parts[5]
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(token_path)
    if not creds or not creds.valid:
        creds = Credentials.from_service_account_file(service_path, scopes=SCOPES)
        '''
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        '''
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=id,
                                    range=range_name).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return
        df = pd.DataFrame(data = values[1:], columns=values)
        x = pd.DataFrame(data = values[1:], columns=values)
        
        
        # loop through the values and save them into the model
        for idx, row in df.iterrows(): # skip the header row
            # extract the data from each row
            
            
            
            
            for colly in x.columns:
                if "overview" in colly[0].lower():  # Case-insensitive check
                    name = colly[0]
            
            
            club_name = row["Name of Club"].iloc[0]
            first_name = row["Your First Name"].iloc[0]
            last_name = row["Your Last Name"].iloc[0]
            description = row[name].iloc[0]

            

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
            
            if dfy:
                return (club_name, leaders, description)
            # create a new club instance and save it
            from display.models import Club
            if " " in email:
                del email
                club = Club(name=club_name, leaders=leaders, description=description, sheet_link=link)
                club.save()
                continue
            club = Club(name=club_name, leaders=leaders, description=description, emails = email, sheet_link=link)
            club.save()
            
        
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    sheet = input("Sheet link for testing: ")
    df = input("Testing Df? (1 for yes) ")
    testing_link = input("Testing Link? (1 for yes)")
    dfing = False
    testing = False
    if int(df) == 1:
        dfing = True
    if int(testing_link) == 1:
        testing = True
    print(main(sheet = sheet, dfy = dfing, testing_link = testing))

        
        
