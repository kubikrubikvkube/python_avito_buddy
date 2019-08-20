import matplotlib.pyplot as plt
import pandas as pd
from pymongo import ASCENDING

from locations import LocationManager
from mongodb import MongoDB
from matplotlib.ticker import FormatStrFormatter

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection
    game_name = "\"iphone\""
    print(f"Trying to find {game_name} in {location_name} city...")
    _filter = {
        "$and": [
            {
                "$text": {
                    "$search": game_name
                }
            },
            {
                "price.value": {
                    "$gte": 3000
                }
            },
            {
                "price.value": {
                    "$lte": 100000
                }
            }
        ]
    }

    found_documents_count = collection.count_documents(_filter)
    print(f"Found {found_documents_count} documents")
    invalid_price_values = ["Цена не указана", "Договорная", "Бесплатно"]
    data = []
    _projection = {
        "_id": 0,
        "uuid": 1,
        "price.value": 1,
        "location": 1
    }
    _sort = [('time', ASCENDING)]

    for ad in collection.find(filter=_filter, projection=_projection, sort=_sort):
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
    print(f"Info: {df.info(verbose=True, memory_usage=True)}")
    print(f"Head: {df.head()}")
    print(f"Describe: {df.describe()}")
    print(f"Price mean: {df['price'].mean()}")
    if df.shape[0] <= 100:
        print(df.to_string())
    plot = df.plot(y="price")
    plot.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.show()