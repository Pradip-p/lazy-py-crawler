import gspread
from oauth2client.service_account import ServiceAccountCredentials

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_doctor_info_to_google_sheet(doctor_info):
    # Define the scope and load credentials from a JSON key file
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    
    # Authorize the client with the loaded credentials
    client = gspread.authorize(creds)
    
    # Open the Google Sheets document by its name
    sheet = client.open('CPSO')
    
    # Select a specific worksheet (e.g., the first one)
    sheet_instance = sheet.get_worksheet(1)

    # Add the item data to the sheet
    values = list(doctor_info.values())
    # append body to spreadsheet
    sheet_instance.append_row(values)
            
    # print("Doctor information added to the Google Sheet.")





if __name__== '__main__':
    # Example usage
    doctor_info = {
        'Name': 'Dr. Jane Smith',
        'Specialty': 'Dermatology',
        'Location': 'Los Angeles',
        'Phone': '987-654-3210'
    }
    save_doctor_info_to_google_sheet(doctor_info)
    save_doctor_info_to_google_sheet(doctor_info)
    
