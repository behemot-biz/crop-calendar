class Plant:
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
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def total_growth_time(self):
        stages = [
            self.germination, self.seedling_stage, self.vegetative_growth,
            self.flowering_root_development, self.fruit_development
        ]
        return sum(stage for stage in stages if stage is not None)

    def summary(self):
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

    # def __str__(self):
    #     return self.summary()


# Subclasses
class Legume(Plant):
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):
        super().__init__(name, category, germination,
                         seedling_stage, vegetative_growth,
                         flowering_root_development,
                         None, description)


class RootVegetable(Plant):
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):
        super().__init__(name, category, germination,
                         seedling_stage, vegetative_growth,
                         flowering_root_development, None, description)


class FruitVegetable(Plant):
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development,
                 fruit_development, description):
        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         fruit_development, description)


class LeafyGreen(Plant):
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):
        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         None, description)


class Bulb(Plant):
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development,
                 fruit_development, description):
        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         fruit_development, description)


class Herb(Plant):
    def __init__(self, name, category, germination, seedling_stage,
                 vegetative_growth, flowering_root_development, description):
        super().__init__(name, category, germination, seedling_stage,
                         vegetative_growth, flowering_root_development,
                         None, description)


def create_plant_instance(plant_data):
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
