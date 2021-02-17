import gspread


scopes = [
    'https://www.googleapis.com/auth/spreadsheets', 
    'https://www.googleapis.com/auth/drive'
]

gc = gspread.service_account(
    filename='./hashcode-gdg-hub-b4166b80f50b.json',
    scopes=scopes
)

myhub_api = "https://hashcode-judge.appspot.com/api/judge/v1/myhub"
sheet_name = 'hashcode-gdg-hub-contestants'
token = ''