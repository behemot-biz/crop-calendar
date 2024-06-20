import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
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

class TableCreator:
    def __init__(self, data_list):
        """
        Initialize the TableCreator with the data list including the header row.

        Args:
            data_list (list): The list of data including the header row.
        """
        self.data_list = data_list
        self.data_items = data_list[1:]  # Exclude the header row
    
    def split_data(self):
        """
        Split the data into two columns.

        Returns:
            tuple: Two lists representing the items in the first and second columns.
        """
        total_list_items = len(self.data_items)
        half_length = (total_list_items + 1) // 2  # Ensure the first column has one more item if odd

        column1 = self.data_items[:half_length]
        column2 = self.data_items[half_length:]

        # If the second column is shorter, pad it with empty strings
        if len(column1) > len(column2):
            column2.append(['', ''])

        return column1, column2
    
    def create_main_table(self):
        """
        Create and return a PrettyTable with data split into two columns.

        Returns:
            PrettyTable: The table with two columns of data.
        """
        column1, column2 = self.split_data()

        # Create a PrettyTable object
        table = PrettyTable()
        # Format PrettyTable
        table.border = False
        table.align = "l"
        table.header = False
        table.padding_width = 5
         
        # Add rows to the PrettyTable, combining id and name as a single string
        for row1, row2 in zip(column1, column2):
            col1_display = f"{row1[0]}. {row1[1]}"
            col2_display = f"{row2[0]}. {row2[1]}" if row2[0] and row2[1] else ""
            table.add_row([col1_display, col2_display])

        return table

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