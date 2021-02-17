import gspead
import requests
import uuid
import hashlib
from config import gc, myhub_api, sheet_name, token

def sheet_task():
    #try:
    #    json_data = get_contestants_data(token)
    #except requests.exceptions.RequestException as e:
    #    print(e)
    sheet = create_sheet()
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    write_data(sheet_instance, json_data)

def get_contestants_data(token):
    headers = {
    'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", myhub_api+'/contestants', 
    headers=headers, data={})
    return response.json()

def create_sheet():
    try:
        sheet = gc.open(sheet_name)
        gc.del_spreadsheet(sheet.id)
        sheet = gc.create(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = gc.create(sheet_name)
    sheet.share('in_boulechfar@esi.dz', perm_type='user', role='writer',
    notify=False)
    return sheet

def write_data(sheet_instance, json_data):
    sheet_instance.insert_row(
        ['uuid', 'hashed_uuid']+[key for key in json_data['items'][0]],
        1
    )
    i = 2
    team_name = ''
    for item in json_data['items']:
        teammate = item['teamName'] == team_name
        if not teammate:
            team_name = item['teamName']
            item_uuid = uuid.uuid4().hex
        row = [
            item_uuid,
            hashlib.md5(item_uuid.encode('utf-8')).hexdigest()
        ] + [item[key] for key in item]
        sheet_instance.insert_row(row, i)
        i += 1


json_data = {
    'items': [
        {
            'email': 'in_boulechfar@esi.dz',
            'firstName': 'Nassim',
            'lastName': 'BOULECHFAR',
            'teamName': 'Bytes'
        },
        {
            'email': 'id_zebbiche@esi.dz',
            'firstName': 'Dhaieddine',
            'lastName': 'ZEBBICHE',
            'teamName': 'Bytes'
        },
        {
            'email': 'im_gouaouri@esi.dz',
            'firstName': 'Mohammeddhiyaeddine',
            'lastName': 'GOUAOURI',
            'teamName': 'Bytes'
        },
        {
            'email': 'ia_chabounia@esi.dz',
            'firstName': 'Aimad',
            'lastName': 'CHABOUNIA',
            'teamName': 'Bytes'
        },
    ]
}

if __name__ == '__main__':
    sheet_task()
