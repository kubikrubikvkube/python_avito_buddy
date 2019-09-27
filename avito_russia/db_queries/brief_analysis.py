from csv_generator import CsvGenerator
from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    mongoDB = MongoDB(location.detailedCollectionName)

    filter = {
        "$and": [
            {
                "userType": "company"
            },
            {
                "$or": [
                    {
                        "parameters.flat.0.description": "Запчасти и аксессуары"
                    },
                    {
                        "parameters.flat.0.description": "Мебель и интерьер"
                    },
                    {
                        "parameters.flat.0.description": "Ремонт и строительство"
                    },
                    {
                        "parameters.flat.0.description": "Одежда, обувь, аксессуары"
                    },
                    {
                        "parameters.flat.0.description": "Предложение услуг"
                    },
                    {
                        "parameters.flat.0.description": "Детская одежда и обувь"
                    },
                    {
                        "parameters.flat.0.description": "Растения"
                    },
                    {
                        "parameters.flat.0.description": "Грузовики и спецтехника"
                    },
                    {
                        "parameters.flat.0.description": "Оборудование для бизнеса"
                    },
                    {
                        "parameters.flat.0.description": "Спорт и отдых"
                    },
                    {
                        "parameters.flat.0.description": "Гаражи и машиноместа"
                    },
                    {
                        "parameters.flat.0.description": "Книги и журналы"
                    },
                    {
                        "parameters.flat.0.description": "Оргтехника и расходники"
                    },
                    {
                        "parameters.flat.0.description": "Телефоны"
                    },
                    {
                        "parameters.flat.0.description": "Товары для компьютера"
                    },
                    {
                        "parameters.flat.0.description": "Аудио и видео"
                    },
                    {
                        "parameters.flat.0.description": "Бытовая техника"
                    },
                    {
                        "parameters.flat.0.description": "Товары для детей и игрушки"
                    },
                    {
                        "parameters.flat.0.description": "Аквариум"
                    },
                    {
                        "parameters.flat.0.description": "Продукты питания"
                    },
                    {
                        "parameters.flat.0.description": "Часы и украшения"
                    },
                    {
                        "parameters.flat.0.description": "Красота и здоровье"
                    },
                    {
                        "parameters.flat.0.description": "Фототехника"
                    },
                    {
                        "parameters.flat.0.description": "Посуда и товары для кухни"
                    },
                    {
                        "parameters.flat.0.description": "Охота и рыбалка"
                    },
                    {
                        "parameters.flat.0.description": "Музыкальные инструменты"
                    },
                    {
                        "parameters.flat.0.description": "Ноутбуки"
                    },
                    {
                        "parameters.flat.0.description": "Велосипеды"
                    },
                    {
                        "parameters.flat.0.description": "Билеты и путешествия"
                    },
                    {
                        "parameters.flat.0.description": "Товары для животных"
                    },
                    {
                        "parameters.flat.0.description": "Планшеты и электронные книги"
                    },
                    {
                        "parameters.flat.0.description": "Настольные компьютеры"
                    },
                    {
                        "parameters.flat.0.description": "Водный транспорт"
                    },
                    {
                        "parameters.flat.0.description": "Игры, приставки и программы"
                    },
                    {
                        "parameters.flat.0.description": "Мотоциклы и мототехника"
                    }
                ]
            },
            {
                "location": {
                    "$geoWithin": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        30.3685284,
                                        59.9135147
                                    ],
                                    [
                                        30.3963375,
                                        59.9187636
                                    ],
                                    [
                                        30.411787,
                                        59.9172148
                                    ],
                                    [
                                        30.4711819,
                                        59.9427175
                                    ],
                                    [
                                        30.4977036,
                                        59.9266355
                                    ],
                                    [
                                        30.4918671,
                                        59.885492
                                    ],
                                    [
                                        30.5179596,
                                        59.8629189
                                    ],
                                    [
                                        30.4983902,
                                        59.8589541
                                    ],
                                    [
                                        30.5636215,
                                        59.8244576
                                    ],
                                    [
                                        30.5062866,
                                        59.8127207
                                    ],
                                    [
                                        30.4218292,
                                        59.8686067
                                    ],
                                    [
                                        30.3685284,
                                        59.9135147
                                    ]
                                ]
                            ]
                        }
                    }
                }
            }
        ]
    }

    distinct_r = mongoDB.find(filter=filter)
    print(f"Unique ads {len(distinct_r)}")
    CsvGenerator.write_into_csv_file(distinct_r, "result.txt", ["phoneNumber"])
