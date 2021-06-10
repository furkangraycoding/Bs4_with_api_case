
# Bu sayfa sadece google seeht api üzerinden veri çekme ve update üzerinedir. Ana proje analytica.py dosyasıdır.

from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE='keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


creds=None
creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID='1LxBkdpHMNjjAT0pam3ImtpI8AaBGlhzQy1F15dHZy6c'

service = build('sheets', 'v4',credentials=creds)

sheet=service.spreadsheets()


result= sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="URL!A1:A1000").execute()


values=result.get('values',[])

print(values[i][0])



aoa=[["1/1/2020","2/2/2020"],["1/1/2020","3/3/2020"]]

request=sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
             range="Sayfa2!B1", valueInputOption="USER_ENTERED", body={"values": aoa}).execute()

print(request)
