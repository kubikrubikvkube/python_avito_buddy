from enum import unique, Enum


@unique
class Location(Enum):
    """
    Географическая локация поиска для Avito
    """
    ALL = (None, None)
    SAINT_PETERSBURG = (653240, 'Санкт-Петербург')
    RUSSIA = (621540, 'Россия')
    MOSCOW = (637640, 'Москва')

    def __init__(self, location_id, location_name):
        self.location_id = location_id
        self.location_name = location_name
