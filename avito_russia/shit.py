import pdb

from locations import LocationManager
from mongodb import MongoDB

if __name__ == '__main__':
    location_name = "SAINT-PETERSBURG"
    location = LocationManager().get_location(location_name)
    collection = MongoDB(location.detailedCollectionName).collection

    coordinates = []

    filter = {
        "userType": "private",
        "location": {
            "$geoWithin": {
                "$geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [
                            30.4109716,
                            60.0529527
                        ],
                        [
                            30.4246187,
                            60.0697657
                        ],
                        [
                            30.4489088,
                            60.0625061
                        ],
                        [
                            30.4301548,
                            60.0464179
                        ],
                        [
                            30.4120445,
                            60.0520957
                        ],
                        [
                            30.4109716,
                            60.0529527
                        ]

                    ]]

                }
            }
        }
    }

    unique_phonenumers = set()
    count = collection.count_documents(filter)
    for document in collection.find(filter):
        if ("phonenumber" in document):
            unique_phonenumers.add(document['phonenumber'])

    print("\n")
    print(len(unique_phonenumers))
   # [print(document) for document in collection.find(filter)]
