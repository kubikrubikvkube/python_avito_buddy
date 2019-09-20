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

    unique_results = mongoDB.find(filter, False)
    print(f"Unique ads {len(unique_results)}")
