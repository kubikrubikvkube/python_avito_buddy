from db_queries import estate_ekb_near_point
from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    mongoDB = MongoDB(location.detailedCollectionName)

    filter = {
        "$and": [
            {
                "userType": "private"
            },
            {
                "location": {
                    "$geoWithin": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        30.454874,
                                        59.9303772
                                    ],
                                    [
                                        30.4600239,
                                        59.934183
                                    ],
                                    [
                                        30.4735851,
                                        59.9317318
                                    ],
                                    [
                                        30.4717398,
                                        59.9260333
                                    ],
                                    [
                                        30.4560757,
                                        59.9297966
                                    ],
                                    [
                                        30.454874,
                                        59.9303772
                                    ],

                                ]
                            ]
                        }
                    }
                }
            }
        ]
    }

    unique_results = mongoDB.find(estate_ekb_near_point, True)
    print(f"Unique ads {len(unique_results)}")
