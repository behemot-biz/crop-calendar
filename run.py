import gspread
from google.oauth2.service_account import Credentials
from classes.table_creator import TableCreator
# from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPPRED_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPPRED_CLIENT.open('crop_calendar')

plants = SHEET.worksheet('plant_list')
data_plants = plants.get_all_values()

# print(data)
def select_plants():
    # Create an instance of TableCreator
    table_creator = TableCreator(data_plants)
    table = table_creator.create_main_table()
    

    print("Welcome to the Crop Calendar Planner!\n")
    print(f"{table} \n\n")

def get_action():
    pass

def get_date():
    pass

def get_selected_plants():
    pass

def store_results():
    pass

user_list_data = select_plants()