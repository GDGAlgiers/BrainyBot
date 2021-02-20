import gspread
import requests
import os
import hashlib
from config import MYHUB_API,PRIVATE_SHEET_NAME


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
    private_sheet = create_sheet(gc, PRIVATE_SHEET_NAME)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    private_sheet_instance = private_sheet.get_worksheet(0)
    write_data(sheet_instance,private_sheet_instance, json_data)


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
    sheet.share('hm_amirouche@esi.dz', perm_type='user',
                role='writer', notify=False)
    print(
        f"Spread Sheet {sheet_name} created and shared you can check this url {sheet.url}")
    return sheet


def write_data(sheet_instance, private_sheet_instance,json_data):
    private_data = []
    contestants_data = []
    contestants_data.append(['hashed_uuid']+[key for key in json_data['items'][0]])
    private_data.append(['uuid', 'hashed_uuid']+[key for key in json_data['items'][0]])
    team_name = ''
    for item in json_data['items']:
        teammate = item['teamName'] == team_name
        if not teammate:
            team_name = item['teamName']
            item_id = os.urandom(8).hex()
            item_uuid = "-".join([item_id[i:i+4]
                                  for i in range(len(item_id)//4)])
            item_hash = hashlib.md5(item_uuid.encode("utf-8")).hexdigest()
        private_row = [
            item_uuid,
            item_hash
        ] + [item[key] for key in item]
        row = [
            item_hash
        ] + [item[key] for key in item]
        private_data.append(private_row)
        contestants_data.append(row)
    try:
        sheet_instance.update(contestants_data)
        private_sheet_instance.update(private_data)
    except gspread.exceptions.APIError as e:
        print(e)
        


if __name__ == '__main__':
    sheet_task()
