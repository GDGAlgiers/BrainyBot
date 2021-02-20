import argparse
import gspread
from config import SCOPES, DEFAULT_SHEET_NAME
from os import path
from sheet_task import sheet_task
my_parser = argparse.ArgumentParser(prog='hash_code_scrapper',
                                    usage='%(prog)s [options] Service_Account [Hub_Token]',
                                    description='Generate identifier for each team and save to a google spreadsheet')

# Add the arguments
my_parser.add_argument('service_account_path',
                       metavar='Service_Account',
                       type=str,
                       help='the path to the json service account')
my_parser.add_argument('--token',
                       action="store",
                       type=str,
                       default=None,
                       help='The token to our hub, it will allow us get participants ')
my_parser.add_argument('--sheet_name',
                       action="store",
                       type=str,
                       default=DEFAULT_SHEET_NAME,
                       help='Google Sheet that we will store the participants ids')

if __name__ == '__main__':

    # Execute the parse_args() method
    args = my_parser.parse_args()
    if path.exists(args.service_account_path):
        # create gspread service account
        gc = gspread.service_account(
            filename=args.service_account_path,
            scopes=SCOPES
        )
        sheet_task(gc, args.sheet_name, args.token)

    else:
        print("[  ERROR  ] The path you have specified don't exist")
