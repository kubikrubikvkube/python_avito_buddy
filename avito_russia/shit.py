from datetime import datetime

import requests
from console_progressbar import ProgressBar

from locations import LocationManager
from mongodb import MongoDB
from settings import GENDER_RESOLVER_HOST

if __name__ == '__main__':
    for location_name in ["MOSCOVSKAYA_OBLAST", "EKATERINBURG", "MOSCOW"]:
        location = LocationManager().get_location(location_name)
        collection = MongoDB(location.detailedCollectionName).collection
        print(f"Processing {location_name}")
        filter = {
            "gender": {
                "$exists": False
            }
        }
        print(f"Started at {datetime.now()}")
        counted_documents = collection.count_documents(filter, hint="gender_1")
        counter = 0
        print(f"Needs to be processed {counted_documents}")
        pb = ProgressBar(total=counted_documents, prefix=location_name, decimals=3, length=50, fill='X', zfill='-')

        for item in collection.find(filter, no_cursor_timeout=True, projection=["uuid", "seller", "seller.name"],
                                    batch_size=100):
            counter += 1
            pb.print_progress_bar(counter)
            if item['uuid'] and 'seller' in item and item['seller']['name']:
                uuid = item['uuid']
                if item['seller']['name']:
                    name_request_json = {
                        "name": item['seller']['name']
                    }
                    r = requests.post(GENDER_RESOLVER_HOST, json=name_request_json)
                    if r.status_code == 200:
                        gender = r.json()['gender']
                        if gender != "UNKNOWN":
                            gender = gender.lower()
                            collection.update_one({"uuid": uuid}, {"$set": {"gender": gender}})
