class UserData:
    """
    A class to store and manage user data including an email
    address and associated data entries.

    Attributes:
    -----------
    _email : str
        The user's email address (protected attribute).
    data : list
        The list of data entries for the user.

    Methods:
    --------
    __init__(email, data=None)
        Initializes the UserData instance with an email
        and an optional data list.
    email : property
        Gets the user's email address.
    add_data(data_entry)
        Adds a new data entry to the user's data list.
    get_data()
        Returns the list of data entries.
    """

    def __init__(self, email, data=None):
        """
        Initializes the UserData instance with an email and an
        optional data list.

        Parameters:
        -----------
        email : str
            The user's email address.
        data : list, optional
            The list of data entries for the user.
            Defaults to an empty list if not provided.
        """
        self._email = email  # Protected attribute
        self.data = data if data is not None else []

    @property
    def email(self):
        """
        Gets the user's email address.

        Returns:
        --------
        str
            The user's email address.
        """
        return self._email

    def add_data(self, data_entry):
        """
        Adds a new data entry to the user's data list.

        Parameters:
        -----------
        data_entry : list
            The data entry to add to the list.
        """
        self.data.append(data_entry)

    def get_data(self):
        """
        Returns the list of data entries.

        Returns:
        --------
        list
            The list of data entries.
        """
        return self.data
