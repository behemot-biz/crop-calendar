from prettytable import PrettyTable


class TableCreator:
    def __init__(self, data_list):
        """
        Initialize the TableCreator with the data list
        including the header row.

        Args:
            data_list (list): The list of data including the header row.
        """
        self.data_list = data_list
        self.data_items = data_list[1:]  # Exclude the header row

    def split_data(self):
        """
        Split the data into two columns.

        Returns:
            tuple: Two lists representing the items in the
            first and second columns.
        """
        total_list_items = len(self.data_items)
        half_length = (total_list_items + 1) // 2

        column1 = self.data_items[:half_length]
        column2 = self.data_items[half_length:]

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

        table = PrettyTable()

        table.border = False
        table.align = "l"
        table.header = False
        table.padding_width = 5

        for row1, row2 in zip(column1, column2):
            col1_display = f"{row1[0]}. {row1[1]}"
            col2_display = (
                f"{row2[0]}. {row2[1]}" if row2[0] and row2[1] else ""
            )
            table.add_row([col1_display, col2_display])

        return table
