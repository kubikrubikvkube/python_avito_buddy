from csv_generator import CsvGenerator
from db_queries import examples
from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    mongoDB = MongoDB(location.detailedCollectionName)

    filter = {
        "$and": [
            {
                "$text": {
                    "$search": "спортивное"
                }
            },
            {
                "userType": "private"
            }
        ]
    }
    distinct_r = mongoDB.find(filter=examples.vasilievskiy_ostrov)
    print(f"Unique ads {len(distinct_r)}")
    CsvGenerator.write_into_csv_file(distinct_r, "result.txt", ["uuid", "phoneNumber", "sellerName", "gender"])
