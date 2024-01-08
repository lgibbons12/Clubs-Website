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
#range_name = 'Form Responses 1!B1:F50'

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to credentials.json
credentials_path = os.path.join(script_dir, 'credentials.json')

token_path = os.path.join(script_dir, "token.json")

service_path = os.path.join(script_dir, 'clubs_key.json')

def get_last_row_and_column(sheet, spreadsheet_id):
    result = sheet.get(spreadsheetId=spreadsheet_id).execute()
    
    properties = result.get('sheets')[0].get('properties')
    last_row = properties.get('gridProperties').get('rowCount')
    last_column = properties.get('gridProperties').get('columnCount')
    return last_row, last_column


def number_to_column_letter(column_number):
    """
    Convert a numeric column index to its corresponding letter(s).
    
    Args:
        column_number (int): The numeric column index (1-based).
        
    Returns:
        str: The corresponding column letter(s).
    """
    # Subtract 1 to make it 0-based for ASCII calculation
    column_number -= 1
    
    # Calculate the first letter (if any)
    first_letter = chr(column_number % 26 + ord('A'))
    
    # Calculate additional letters (if needed)
    additional_letters = ""
    while column_number >= 26:
        column_number //= 26
        additional_letters = chr(column_number % 26 + ord('A') - 1) + additional_letters
    
    return additional_letters + first_letter
def main(sheet = None, dfy = False, testing_link = False):
    with open('link.txt', 'w') as f:
        f.write(sheet)


    parts = sheet.split("/")
    
    id = parts[5]
    
    if testing_link:
        return id
    creds = None
    #if os.path.exists('token.json'):
        #creds = Credentials.from_authorized_user_file(token_path)
    #if not creds or not creds.valid:
    creds = Credentials.from_service_account_file(service_path, scopes=SCOPES)
    if True:
        pass
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
        last_row, last_column = get_last_row_and_column(sheet, id)
        start_col = 'B'
        end_col = number_to_column_letter(last_column)
        range_name = f'Form Responses 1!{start_col}1:{end_col}{last_row}'
        # Construct the range dynamically
        
        
        result = sheet.values().get(spreadsheetId=id, range=range_name).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return
        
        #make sure all lists inside values are the same length
        max_len = max(len(sublist) for sublist in values)
        values = [sublist + [None] * (max_len - len(sublist)) for sublist in values]

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
            email = row["Email Address"].iloc[0]
            description = row[name].iloc[0]

            

            # reformat the data according to your rules
            if '/' in first_name:
                # Split first_name and last_name by "/"
                first_name_parts = first_name.split('/')
                last_name_parts = last_name.split('/')

                # Construct leaders string
                leaders = first_name_parts[0] + " " + last_name_parts[0] + ", " + first_name_parts[1] + " " + last_name_parts[1]

               
            else:
                leaders = first_name + " " + last_name # concatenate first and last name
  
            if dfy:
                return (club_name, leaders, description)
            # create a new club instance and save it
            
            from display.models import Club
            
            club = Club(name=club_name, leaders=leaders, description=description, emails = email, sheet_link=link, approved = True)
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

        
        
