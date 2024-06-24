import gspread
from google.oauth2.service_account import Credentials
from classes.table_creator import TableCreator
from datetime import datetime, timedelta
from classes.plant import Plant
from prettytable import PrettyTable
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


def clear_terminal():
    """
    Clear the terminal screen.
    """
    if platform.system == "windows":
        os.system("cls")
    else:
        os.system("clear")


def display_menu(options):
    """
    Display a menu of options and return the user's choice.

    Args:
        options (list): A list of menu options.

    Returns:
        int: The user's selected option.
    """
    clear_terminal()
    print("Menu:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("enter your choice: ").strip())
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Invalid input,please enter a number")


def main_menu():
    """
    Display the main menu and handle user selection.
    """
    options = ["Plan crops", "View stored data", "Exit"]
    while True:
        choice = display_menu(options)
        if choice == 1:
            plan_crops()
        elif choice == 2:
            view_stored_data()
        elif choice == 3:
            print("Thank you for using the Crop Calendar Planner!")
            break


def welcome_message():
    """
    Display the welcome message and introduction to using the
    Crop Calendar Planner app.
    """
    clear_terminal()
    print("Welcome to the Crop Calendar Planner!")
    print(
        "\n This application is designed to help you plan your planting and "
        " harvesting times efficiently. Whether you're a seasoned gardener or "
        " just starting out, this tool will guide you through the process of "
        " determining the best dates for planting and harvesting your crops."
        "\n\nQuick guide:"
        "\n1. You will be presented with a list of plants to choose from."
        "\n2. Select the plants you're interested in by entering their "
        "corresponding numbers."
        "\n3. Decide whether you want to input a planting date or a desired "
        "harvest date."
        "\n4. Enter the date, and the app will calculate the corresponding "
        "planting or harvest dates for you."
        "\n5. You can save the results for future reference by providing your "
        "email address."
        "\n6. You can also view your previously stored data."
        "\n\nLet's get started and make your gardening experience more "
        "organized and productive!"
    )
    input("\nPress Enter to continue...")


def plan_crops():
    """
    Function to plan crops by selecting plants and calculating dates.
    """
    # print("plan crops option")
    user_list = select_plants()
    if user_list:
        user_list_data, action, results = get_selected_plants(
            data_plants, user_list
        )
        print("\nResults:\n")
        print(results)
        store_data_prompt(user_list_data)


def view_stored_data():
    """
    Function to view stored data by entering the user's email.
    """
    email = input(
        "Please enter your email address to fetch your stored data: "
    ).strip()
    user_data = fetch_user_data(email)
    display_user_data(user_data)
    input("\nPress Enter to return to the main menu...")


def select_plants():
    """
    Display a table of plants and allow the user to select multiple
    plants by entering their numbers.

    Returns:
        list: A list of selected plant indices.
    """
    clear_terminal()
    table_creator = TableCreator(data_plants)
    table = table_creator.create_main_table()

    print(f"{table} \n")
    print("Type in the plant number from the list above, if you want multiple")
    print("plants, use comma sign to separate them. Example: 1,8,12\n")

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
                print(f"IndexError: The item {idx} does not exist,")
                print(f"select a number from the list.")
                valid_input = False
                break
            except ValueError:
                print(f"Invalid input '{plant_id}'.")
                print(f"Please enter numbers only.")
                valid_input = False
                break

        if valid_input:
            clear_terminal()
            return user_list


def get_action():
    """
    Prompt the user to choose between entering a
    planting date or a harvest date.

    Returns:
        str: 'P' for planting or 'H' for harvest.
    """
    while True:
        action = input(
            "Do you want to plan for planting seeds (P) "
            "or a date for harvest (H)?\n"
        ).strip().upper()

        if action in ['P', 'H']:
            return action
        else:
            print("Invalid choice.")
            print("Please enter 'P' for planting or 'H' for harvest.")


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
            return date_str
        except ValueError:
            print("Invalid date format.")
            print("Please enter the date in YYYY-MM-DD format.")


def get_selected_plants(data, user_selection):
    """
    Calculate and display planting or harvest dates based on
    user selection.

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

    matching_rows = [
        data_dict[str(id)]
        for id in user_selection
        if str(id) in data_dict
    ]

    plants = [Plant(*row) for row in matching_rows]

    results = PrettyTable()
    results.border = False
    results.align = "l"
    results.padding_width = 5

    user_list_data = []

    if action == 'P':
        results.field_names = [
            "Plant", "Planting Date", "Estimated Harvest Date"
        ]
        for plant in plants:
            harvest_date = input_date + timedelta(
                days=plant.total_growth_time()
            )
            results.add_row([
                plant.name,
                input_date.strftime('%Y-%m-%d'),
                harvest_date.strftime('%Y-%m-%d')
            ])
            user_list_data.append([
                plant.name, "Planting Date",
                input_date.strftime('%Y-%m-%d'),
                harvest_date.strftime('%Y-%m-%d')
            ])

        print("\nPlanting Schedule: \n")
        print(results)

    elif action == 'H':
        results.field_names = [
            "Plant", "Estimated Planting Date", "Harvest Date"
        ]
        for plant in plants:
            planting_date = input_date - timedelta(
                days=plant.total_growth_time()
            )
            results.add_row([
                plant.name,
                planting_date.strftime('%Y-%m-%d'),
                input_date.strftime('%Y-%m-%d')
            ])
            user_list_data.append([
                plant.name, "Harvest Date",
                input_date.strftime('%Y-%m-%d'),
                planting_date.strftime('%Y-%m-%d')
            ])

        print("\nHarvest Schedule:\n")
        print(results)

    return user_list_data, action, results


def store_data_prompt(user_list_data):
    """
    Prompt the user to store data and handle the storage process.

    Args:
        user_list_data (list): The list of data to store.
    """
    store_choice = input(
        "\nDo you want to store this data? (Y/N): "
    ).strip().upper()

    if store_choice == 'Y':
        email = input("Enter your email address: ").strip()
        store_results(email, user_list_data)
        print("Data has been stored successfully.")
    else:
        print("Data was not stored.")


def store_results(email, results):
    """
    Store the user's results in the 'user_results' worksheet.

    Args:
        email (str): The user's email address.
        results (list): The list of results to store.
    """
    results_sheet = SHEET.worksheet('user_results')

    if len(results_sheet.get_all_values()) == 0:
        results_sheet.append_row([
            "Email", "Plant", "Date Type", "Date", "Corresponding Date"
        ])

    for result in results:
        results_sheet.append_row([email] + result)


def fetch_user_data(email):
    """
    Fetch user data from the 'user_results' worksheet
    based on the provided email address.

    Args:
        email (str): The user's email address.

    Returns:
        list: A list of user data records.
    """
    results_sheet = SHEET.worksheet('user_results')

    all_records = results_sheet.get_all_records()

    user_data = [
        record for record in all_records
        if record['Email'] == email
    ]

    return user_data


def display_user_data(user_data):
    """
    Display the user's stored data in a formatted table.

    Args:
        user_data (list): The list of user data records.
    """
    if not user_data:
        print("No data found for the provided email address.")
        return
    results = PrettyTable()
    results.field_names = [
        "Plant", "Date Type", "Date", "Corresponding Date"
    ]

    for record in user_data:
        results.add_row([
            record["Plant"],
            record["Date Type"],
            record["Date"],
            record["Corresponding Date"]
        ])

    print("\nYour Stored Data:\n")
    print(results)


if __name__ == "__main__":
    welcome_message()
    main_menu()
