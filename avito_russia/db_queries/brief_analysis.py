import matplotlib.pyplot as plt
import pandas as pd

from locations import LocationManager
from mongodb import MongoDB
from matplotlib.ticker import FormatStrFormatter

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection
    game_name = "a way out"
    print(f"Trying to find {game_name} in {location_name} city...")
    filter = {
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
                "price.value": {
                    "$lte": 4000
                }
            },
            {
                "price.value": {
                        "$gte": 150
                    }
            }
        ]
    }

    found_documents_count = collection.count_documents(filter)
    print(f"Found {found_documents_count} documents")
    invalid_price_values = ["Цена не указана", "Договорная", "Бесплатно"]
    data = []
    collection.find(filter=filter,projection={
        "_id": 0,
        "uuid": 1,
        "price.value": 1,
        "location": 1
    })
    for ad in collection.find(filter):
        uuid = ad['uuid']
        raw_price = ad['price']['value']
        if type(raw_price) is int:
            price = raw_price
        else:
            price = None

        lat = ad['location']['coordinates'][1]
        lng = ad['location']['coordinates'][0]
        data.append([uuid, price, lat, lng])
    df = pd.DataFrame(data, columns=["uuid", "price", "lat", "lng"])

    #plot = df.plot(y="price")
    #plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    #plt.show()
    print(df.info(verbose=True, memory_usage=True))
    print(df.head())
    print(df.describe())
    if df.shape[0] <= 100:
        print(df.to_string())
