import gspread
from google.oauth2.service_account import Credentials
from classes.table_creator import TableCreator
from datetime import datetime, timedelta
from classes.plant import Plant
from prettytable import PrettyTable
# clear terminal
import os
import platform

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

def select_plants():
    """
    Display a table of plants and allow the user to select multiple plants by entering their numbers.
    
    Returns:
        list: A list of selected plant indices.
    """
    
    table_creator = TableCreator(data_plants)
    table = table_creator.create_main_table()
    
    print("Welcome to the Crop Calendar Planner!\n")
    print(f"{table} \n")
    print("Type in the plant number from the list above, if you want multiple plants, ")
    print("use comma sign to separate them. Example: 1,8,12\n")
    
    while True:
        data_str = input("Enter one or more plant numbers: \n")

        selected_plants = data_str.split(",")
        user_list = []
        valid_input = True

        for plant_id in selected_plants:
            
            try:
                idx = int(plant_id.strip())
                if str(idx) in data_plants[idx][0]:
                    user_list.append(idx)

            except IndexError:
                print(f"IndexError: The item {idx} does not exist, select a number from the list.")
                valid_input = False
                break
            
            except ValueError:
                print(f"Invalid input '{plant_id}'. Please enter numbers only.")
                valid_input = False
                break

        if valid_input:
            clear_terminal()
            return user_list

def get_action():
    """
    Prompt the user to choose between entering a planting date or a harvest date.
    
    Returns:
        str: 'P' for planting or 'H' for harvest.
    """
    while True:
        action = input("Do you want to enter a date for planting seeds (P) or a date for harvest (H)? \n").strip().upper()
        if action in ['P', 'H']:
            return action
        else:
            print("Invalid choice. Please enter 'P' for planting or 'H' for harvest.")

def get_date():
    """
    Prompt the user to enter a date and validate the format.
    
    Returns:
        str: A valid date string in YYYY-MM-DD format.
    """
    while True:
        date_str = input("Enter the date (YYYY-MM-DD): \n").strip()
        try:
            input_date = datetime.strptime(date_str, "%Y-%m-%d")
            return date_str  # Exit the loop if date is valid
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def get_selected_plants(data, user_selection):
    """
    Calculate and display planting or harvest dates based on user selection.
    
    Args:
        data (list): The list of plant data from the Google Sheet.
        user_selection (list): The list of selected plant indices.
    
    Returns:
        tuple: Contains user_list_data, action, and results table.
    """

    action = get_action()
    date_str = get_date()

    input_date = datetime.strptime(date_str, "%Y-%m-%d")
      
    data_dict = {row[0]: row for row in data}
    matching_rows = [data_dict[str(id)] for id in user_selection if str(id) in data_dict]
    plants = [Plant(*row) for row in matching_rows]

    results = PrettyTable()
    results.border = False
    results.align = "l"
    results.padding_width = 5

    user_list_data = []
    
    if action == 'P':
        results.field_names = ["Plant", "Planting Date", "Estimated Harvest Date"]
        for plant in plants:
            harvest_date = input_date + timedelta(days=plant.total_growth_time())
            results.add_row([plant.name, input_date.strftime('%Y-%m-%d'), harvest_date.strftime('%Y-%m-%d')])
            user_list_data.append([plant.name, "Planting Date", input_date.strftime('%Y-%m-%d'), harvest_date.strftime('%Y-%m-%d')])
        
        print("\nPlanting Schedule: \n")
        print(results)

    elif action == 'H':
        results.field_names = ["Plant", "Estimated Planting Date", "Harvest Date"]
        for plant in plants:    
            planting_date = input_date - timedelta(days=plant.total_growth_time())
            results.add_row([plant.name, planting_date.strftime('%Y-%m-%d'), input_date.strftime('%Y-%m-%d')])
            user_list_data.append([plant.name, "Harvest Date", input_date.strftime('%Y-%m-%d'), planting_date.strftime('%Y-%m-%d')])
        
        print("\nHarvest Schedule:\n")
        print(results)
    
    store_choice = input("\nDo you want to store this data? (Y/N): ").strip().upper()
    if store_choice == 'Y':
        email = input("Enter your email address: ").strip()
        store_results(email, user_list_data)
        print("Data has been stored successfully.")
    else:
        print("Data was not stored.")
    return user_list_data, action, results

def store_results(email, results):
    """
    Store the user's results in the 'user_results' worksheet.
    
    Args:
        email (str): The user's email address.
        results (list): The list of results to store.
    """
    
    results_sheet = SHEET.worksheet('user_results')
    
    if len(results_sheet.get_all_values()) == 0:
        results_sheet.append_row(["Email", "Plant", "Date Type", "Date", "Corresponding Date"])
    
    for result in results:
        results_sheet.append_row([email] + result)
    

def clear_terminal():
    """
    Clear the terminal screen.
    """
    if platform.system == "windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    """
    Main function to run the Crop Calendar Planner application.
    """
    while True:
        clear_terminal()
        user_list = select_plants()
        user_list_data = get_selected_plants(data_plants, user_list)
        # store_results(user_list_data)
    
        repeat = input("\nDo you want to add more plants? (Y/N): ").strip().upper()
        if repeat != 'Y':
            print("Thank you for using the Crop Calendar Planner!")
            break

main()


