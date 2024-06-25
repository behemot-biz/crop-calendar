class Plant:
    """
    A class to represent a plant with its growth stages and description.

    Attributes:
    -----------
    id : str
        The plant's unique identifier.
    name : str
        The name of the plant.
    category : str
        The category of the plant.
    germination : int or None
        The number of days for the germination stage.
    seedling_stage : int or None
        The number of days for the seedling stage.
    vegetative_growth : int or None
        The number of days for the vegetative growth stage.
    flowering_root_development : int or None
        The number of days for the flowering/root development stage.
    fruit_development : int or None
        The number of days for the fruit development stage.
    description : str
        A brief description of the plant.

    Methods:
    --------
    parse_int(value)
        Converts a value to an integer, returns None if conversion fails.
    total_growth_time()
        Calculates the total growth time of the plant.
    summary()
        Provides a summary of the plant's attributes.
    """

    def __init__(self, id, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development,
                 fruit_development, description):

        self.id = id
        self.name = name
        self.category = category
        self.germination = self.parse_int(germination)
        self.seedling_stage = self.parse_int(seedling_stage)
        self.vegetative_growth = self.parse_int(vegetative_growth)
        self.flowering_root_development = self.parse_int(
            flowering_root_development
        )
        self.fruit_development = self.parse_int(fruit_development)
        self.description = description

    def parse_int(self, value):
        """
        Converts a value to an integer, returns None if conversion fails.

        Parameters:
        -----------
        value : str or int
            The value to convert to an integer.

        Returns:
        --------
        int or None
            The converted integer or None if conversion fails.
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def total_growth_time(self):
        """
        Calculates the total growth time of the plant.

        Returns:
        --------
        int
            The total number of days for all growth stages.
        """
        stages = [
            self.germination, self.seedling_stage, self.vegetative_growth,
            self.flowering_root_development, self.fruit_development
        ]
        return sum(stage for stage in stages if stage is not None)

    def summary(self):
        """
        Provides a summary of the plant's attributes.

        Returns:
        --------
        str
            A string summary of the plant's attributes.
        """
        return (
            f"Plant: {self.name}\n"
            f"Category: {self.category}\n"
            f"Germination Time: {self.germination or 'N/A'} days\n"
            f"Seedling Stage Time: {self.seedling_stage or 'N/A'} days\n"
            f"Vegetative Growth Time: {self.vegetative_growth or 'N/A'} days\n"
            f"Flowering/Root Development Time: "
            f"{self.flowering_root_development or 'N/A'} days\n"
            f"Fruit Development Time: {self.fruit_development or 'N/A'} days\n"
            f"Total Growth Time: {self.total_growth_time()} days\n"
            f"Description: {self.description}"
        )


class Legume(Plant):
    """
    A class to represent a legume, a type of plant.

    Inherits from the Plant class.
    """
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):

        super().__init__(name, category, germination,
                         seedling_stage, vegetative_growth,
                         flowering_root_development,
                         None, description)


class RootVegetable(Plant):
    """
    A class to represent a root vegetable, a type of plant.

    Inherits from the Plant class.
    """
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):

        super().__init__(name, category, germination,
                         seedling_stage, vegetative_growth,
                         flowering_root_development, None, description)


class FruitVegetable(Plant):
    """
    A class to represent a fruit vegetable, a type of plant.

    Inherits from the Plant class.
    """
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development,
                 fruit_development, description):

        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         fruit_development, description)


class LeafyGreen(Plant):
    """
    A class to represent a leafy green, a type of plant.

    Inherits from the Plant class.
    """
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):

        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         None, description)


class Bulb(Plant):
    """
    A class to represent a bulb, a type of plant.

    Inherits from the Plant class.
    """
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development,
                 fruit_development, description):

        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         fruit_development, description)


class Herb(Plant):
    """
    A class to represent an herb, a type of plant.

    Inherits from the Plant class.
    """
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):

        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         None, description)


def create_plant_instance(plant_data):
    """
    Creates a plant instance from a dictionary of plant data.

    Parameters:
    -----------
    plant_data : dict
        A dictionary containing plant data with keys
        corresponding to plant attributes.

    Returns:
    --------
    tuple
        A tuple containing the plant attributes.
    """
    id = plant_data["id"]
    name = plant_data["Name"]
    category = plant_data["Category"]
    germination = plant_data["Germination"]
    seedling_stage = plant_data["Seedling Stage"]
    vegetative_growth = plant_data["Vegetative Growth"]
    flowering_root_development = plant_data["Flowering/Root Development"]
    fruit_development = plant_data["Fruit Development"]
    description = plant_data.get("Description", "")

    return (
        id, name, category, germination, seedling_stage, vegetative_growth,
        flowering_root_development, fruit_development, description
    )
