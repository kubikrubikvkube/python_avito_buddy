import matplotlib.pyplot as plt
import pandas as pd
from bson import ObjectId
from console_progressbar import ProgressBar

from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "MOSCOW"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection

    filter = {
        "$and": [
            {
                "price.value": {
                    "$exists": True
                }
            },
            {
                "price.value": {
                    "$type": 2
                }
            }
        ]
    }

    print("Started")

    invalid_price_values = ["Цена не указана", "Договорная", "Бесплатно", "Зарплата не указана"]
    not_processed_count = collection.count_documents(filter)
    counter = 0
    print(f"Not processed {not_processed_count}")
    pb = ProgressBar(total=not_processed_count, decimals=3, length=50, fill='X', zfill='-')
    for item in collection.find(filter):
        if item['price']['value']:
            raw_price = item['price']['value']
            if not invalid_price_values.count(raw_price) and type(raw_price) is str:
                price = int(raw_price.replace(" ", ""))
                collection.update_one({
                    "_id": ObjectId(str(item['_id']))
                }, {
                    "$set": {"price.value": price}
                })
        counter += 1
        pb.print_progress_bar(counter)
        # print(f"Processed {counter} items last one has uuid {item['uuid']}")

    print("All done")
