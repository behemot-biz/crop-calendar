import gspread
from google.oauth2.service_account import Credentials
from classes.table_creator import TableCreator


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
    print("Type in the plant number from the list above, if you want multiple plants, ")
    print("use comma sign to separate them.\n")
    print("Example: 1,7,8,12\n")
    while True:
        data_str = input("Enter your numbers here: ")
        # print(f"Numbers entered are: {data_str} \n\n")

        selected_plants = data_str.split(",")
        user_list = []
        valid_input = True

        for plant_id in selected_plants:
            # print(data_plants)
            try:
                idx = int(plant_id.strip())  # Strip any extra whitespace
                if str(idx) in data_plants[idx][0]:
                    user_list.append(idx)

            except IndexError:
                # Handle the IndexError if the index is out of range
                print(f"IndexError: The item {idx} does not exist, select a number from the list.")
                valid_input = False
                break
            
            except ValueError:
                print(f"Invalid input '{plant_id}'. Please enter numbers only.")
                valid_input = False
                break

        if valid_input:
            print(f"userlist {user_list}. Operation success")
            
            return user_list

def get_action():
    pass

def get_date():
    pass

def get_selected_plants():
    pass

def store_results():
    pass


user_list_data = select_plants()