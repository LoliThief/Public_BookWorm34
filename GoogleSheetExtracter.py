# PIP libraries
from googleapiclient.discovery import build
from google.oauth2 import service_account

values = []

def initiate():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'key.json'

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    SAMPLE_SPREADSHEET_ID = '1yz2XETooQNGtfE0Bk_loj2mp0wquPG6EAPsoyulNXeI'

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Sheet1!A1:AN100").execute()
    global values
    values = result.get('values', [])

def get_value(row, column):
    try:
        i = values[row-1][column-1]
        if(i == '' or i == " "):
            return 0
        return i
    except:
        return 0

def book_by_skill(skill):
    where_look = 0
    for i in values[1]:
        if(i == skill):
            break
        where_look += 1

"""
for i in values[0]:
    if (i == ''):
        continue
    else:
        #print(i, end = ", ")
"""

"""
initiate()
print(values)
"""