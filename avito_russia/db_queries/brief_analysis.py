from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    mongoDB = MongoDB(location.detailedCollectionName)

    filter = {
        "$and": [
            {"parameters.flat.description": "Игры для приставок"},
            {"userType": "private"},
            {"phoneNumber": {"$exists": True}}
        ]
    }

    found_ads = list(mongoDB.collection.find(filter=filter))
    print(f"Non-unique ads {len(found_ads)}")
    unique_ads = mongoDB.filter_unique_phoneNumbers(found_ads)
    print(f"Unique ads {len(unique_ads)}")
