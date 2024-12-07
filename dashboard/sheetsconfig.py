import gspread
from google.oauth2.service_account import Credentials

def export_to_google_sheets(data):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file(
        '../credentials1.json', scopes=SCOPES
    )
    client = gspread.authorize(credentials)

    # Google Sheets faylini oching yoki yangi yarating
    spreadsheet_name = 'Quiz Results'
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)

    # Birinchi varaqqa ulaning
    sheet = spreadsheet.sheet1

    # Sarlavhalarni yozing
    headers = ['Ismi', 'Telefon', 'Email', 'Savollar', 'To‘g‘ri', 'Xato']
    sheet.clear()  # Avvalgi ma'lumotlarni o'chirish
    sheet.append_row(headers)

    # Ma'lumotlarni yozish
    for row in data:
        sheet.append_row(row)

    print("Google Sheets-ga muvaffaqiyatli eksport qilindi!")
