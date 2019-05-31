from enum import unique, Enum


@unique
class Category(Enum):
    ALL = (None, None)
    TRANSPORT = (1, 'Транспорт')
    REALTY = (4, 'Недвижимость')
    AUTOMOBILES = (9, 'Автомобили')
    FLATS = (24, 'Квартиры')
    PETS = (35, 'Домашние животные')

    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name
