import matplotlib.pyplot as plt
import pandas as pd

from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection
    game_name = "god of war"
    cursor = collection.find({
        "$and": [
            {
                "$text": {
                    "$search": game_name
                }
            },
            {
                "parameters.flat.description": "Игры, приставки и программы"
            },
            {
                "userType": "private"
            }
        ]
    }, {
        "_id": 0,
        "uuid": 1,
        "price.value": 1,
        "location": 1
    })

    invalid_price_values = ["Цена не указана", "Договорная", "Бесплатно"]
    data = []
    for ad in cursor:
        uuid = ad['uuid']
        raw_price = ad['price']['value']
        if not invalid_price_values.count(raw_price):
            price = int(raw_price.replace(" ", ""))
        else:
            price = None

        lat = ad['location']['coordinates'][1]
        lng = ad['location']['coordinates'][0]
        data.append([uuid, price, lat, lng])
    df = pd.DataFrame(data, columns=["uuid", "price", "lat", "lng"])
    print(df.describe())
    print("\n")
    print(df.head())
    plt.show()
