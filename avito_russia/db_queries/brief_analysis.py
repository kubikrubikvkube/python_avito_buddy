from db_queries.geo import vasilievskiy_ostrov
from db_queries.people import males, persons
from locations import LocationManager
from mongodb import MongoDB


if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    mongoDB = MongoDB(location.detailedCollectionName)

    filter = {
        "$and": [
            vasilievskiy_ostrov,
            males,
            persons
        ]

    }

    distinct_r = mongoDB.find(filter=filter)
    print(f"Unique ads {len(distinct_r)}")
    name = "himki"
    # CsvGenerator.write_into_csv_file(distinct_r, f"{name}_{len(distinct_r)}.txt", ["phoneNumber"])
