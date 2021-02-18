import gspread
import requests
import uuid
import hashlib
from config import MYHUB_API


def sheet_task(gc, sheet_name, token=None):
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
    if token != None:
        try:
            json_data = get_contestants_data(token)
        except requests.exceptions.RequestException as e:
            print(e)
    sheet = create_sheet(gc, sheet_name)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    write_data(sheet_instance, json_data)


def get_contestants_data(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", f'{MYHUB_API}/contestants',
                                headers=headers, data={})
    return response.json()


def create_sheet(gc, sheet_name):
    try:
        sheet = gc.open(sheet_name)
        gc.del_spreadsheet(sheet.id)
        sheet = gc.create(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = gc.create(sheet_name)
    sheet.share('ha_boutouchent@esi.dz', perm_type='user',
                role='writer', notify=False)
    print(
        f"Spread Sheet created and shared you can check this url {sheet.url}")
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
            item_hash = hashlib.md5(item_uuid.encode('utf-8')).hexdigest()
        row = [
            item_uuid,
            item_hash
        ] + [item[key] for key in item]
        sheet_instance.insert_row(row, i)
        i += 1


if __name__ == '__main__':
    sheet_task()